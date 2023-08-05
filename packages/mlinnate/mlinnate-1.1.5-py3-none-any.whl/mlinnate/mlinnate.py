#Innate main library

import time,datetime,dill,inspect,base64,json,random,rpyc
import collections,h5py,getpass,glob,os,codecs,pickle,__main__
import numpy as np
import matplotlib.pyplot as plt
from IPython import get_ipython

################################ EARLY STOPPERS ###############################

"""Stop the training if the difference between the evaluator "eval_name" value and the previous one is under the "gap" for "threshold" consecutive time"""
class fixed_gap():
    def __init__(self,args):
        self.eval_name=args[0]
        self.gap=args[1]
        self.threshold=args[2]
        self.ft=1     
    def testing(self,eval_values):
        if self.ft==1:
            self.cnt=0
            self.ft=0
        else:
            cur=eval_values[self.eval_name][-1]
            pred=eval_values[self.eval_name][-2]
            if np.abs(pred-cur)<self.gap:
                self.cnt+=1
                #print("stagnation detected (%d)"%(self.cnt))
            else:
                #print("reset counter")
                self.cnt=0
            if self.cnt>=self.threshold:
                print("fixed gap : early stopping on value %f"%(cur))
                return True
            else:
                return False

"""Stop the training if the evaluator "eval_name" value goes under the "threshold" """
class fixed_threshold():
    def __init__(self,args):
        self.eval_name=args[0]
        self.threshold=args[1]
    def testing(self,eval_values):
        values=eval_values[self.eval_name]
        if values==[]:
            return False
        cur=values[-1]
        if cur<self.threshold:
            print("fixed threshold : early stopping on value %f"%(cur))
            return True
        else:
            return False
        
"""Stop the training if the mean on a sliding window of size "window_size" of evaluator "eval_name" value goes under the "threshold" """
class window_threshold():
    def __init__(self,args):
        self.eval_name=args[0]
        self.window_size=args[1]
        self.threshold=args[2]
    def testing(self,eval_values):
        m=np.mean(eval_values[self.eval_name][-self.window_size:])
        #print("mean value=%f"%(m))
        if m<self.threshold:
            print("window threshold : early stopping on value %f"%(m))
            return True
        else:
            return False

################################ EVALUATORS ###################################

#keras versions

"""evaluate the loss value of the network on the validation set"""
def float_precision_keras(net,trainer,val_input,val_output):
    res=net.predict(val_input)
    vprecision=np.abs(res-val_output)
    precision=sum(vprecision)/val_output.size
    res=precision[0] 
    #print("eval=%f"%(res))
    return res

"""evaluate the loss value of the network on training set"""
def loss_function_keras(net,trainer,val_input,val_output):
    return trainer.get_loss()


#torch versions

"""evaluate the loss value of the network on the validation set"""
def float_precision_torch(net,val_input,val_output,loss_values):
    res=net(val_input)
    vprecision=np.abs(res.cpu().detach().numpy()-val_output.cpu().detach().numpy())
    precision=sum(vprecision)/val_output.size()
    res=precision[0] 
    return res

"""evaluate the loss value of the network on training set"""
def loss_function_torch(net,val_input,val_output,loss_values):
    return loss_values[-1]

########################### LEARN RATE ADAPTERS ################################

def exponential_lra(old_value,args,epoch):
    coef=args[0]
    new_value=old_value*coef
    #print("update lr old value %f new value %f"%(old_value,new_value))
    return new_value

def fixed_lra(old_value,args,epoch):
    new_value=args[0]
    return new_value

############################### TRAINING FUNCTIONS #############################




def setup_keras(conn,tid,task):
    import keras
    from keras import backend as K
    import tensorflow as tf
    #global config,sess

    config=tf.ConfigProto(intra_op_parallelism_threads=1,inter_op_parallelism_threads=1)
    vseed=1
    tf.compat.v1.random.set_random_seed(vseed)
    #dont allow tf to pre-allocate all memory
    config.gpu_options.allow_growth=True
    #set limit on memory usage
    config.gpu_options.per_process_gpu_memory_fraction=0.95
    #affect config to keras session
    sess=tf.Session(graph=tf.get_default_graph(),config=config)
    K.tensorflow_backend.set_session(sess)


def train_keras(conn,tid,task):
    epoch_shift=0
    #read the data from file
    target_input,target_output,val_input,val_output=read_data(task["data_file"])

    #init time
    begin_time=time.time()

    #init results array
    loss_values=[]
    val_loss_values=[]
    es_values=[0]

    #communicate with scheduler
    try:
        conn.root.start(tid)
    except:
        pass

    #create a callback
    from innate_keras_callback import inn_callback
    custom_callback=inn_callback()

    #instanciate the target network
    target_net=keras.models.load_model(task["model_file"])

    #calculate the checkpoint period
    if task["cp_freq"]==None:
        step=None
    else:
        step=int(task["nb_epochs"]*task["cp_freq"]/100)

    #initialize the evaluator
    evaluator=task["evaluator"]
    eval_values={}
    for nevl in evaluator.keys():
        eval_values[nevl]=[]

    #initialize the early stopping
    if task["es"]!=None:
        stopper=task["es"](task["es_args"])
    else:
        stopper=None

    #initialize the learning rate adapter
    if task["lra"]!=None:
        target_lra_args=task["lra_args"]
        target_update_lr=task["lra"]
    else:
        target_update_lr=None
        target_lra_args=None

    #passing the parameters to the callback
    custom_callback.set_cb_params(tid,conn,step,epoch_shift,target_net,task["results_folder"],eval_values,loss_values,val_loss_values,es_values,val_input,val_output,evaluator,stopper,target_update_lr,target_lra_args)
    
    #train the network
    hist=target_net.fit(target_input,target_output,epochs=task["nb_epochs"],verbose=0,callbacks=[custom_callback],batch_size=task["batch_size"],validation_data=(val_input,val_output))
    
     
    #save result network 
    res_net_name="%s/%s_res.wei"%(task["results_folder"],tid)
    #print("saving net in %s"%(res_net_name))
    target_net.save(res_net_name)

    #save other results
    res_data_name="%s/%s_res.h5"%(task["results_folder"],tid)
    write_result_file(res_data_name,eval_values,loss_values,val_loss_values)

    #end timer and store result
    end_time=time.time()
    elapsed_time=end_time-begin_time
    etime=str(datetime.timedelta(seconds=elapsed_time))
    #print("elapsed time : ",etime_str)

    #stdout & stderr file setting
    stdout_name="%s/%s.stdout"%(task["results_folder"],tid)
    stderr_name="%s/%s.stderr"%(task["results_folder"],tid)

    #build result string
    result=dict_serialize({"res_net_name":res_net_name,"res_data_name":res_data_name,"stdout_name":stdout_name,"stderr_name":stderr_name,"etime":etime,"last_epoch":es_values[0]})

    #remove all temporary saves
    filelist=glob.glob("%s/%s_checkpoint_*.wei"%(task["results_folder"],tid))
    for f in filelist:
        os.remove(f)

    #communicate with scheduler
    print("training complete for job %s"%(tid))
    conn.root.stop(tid,result)


########################### PYTORCH ##########################################

def setup_pytorch(conn,tid,task):
    pass


def train_pytorch(conn,tid,task):
    epoch_shift=0
    #read the data from file
    target_input,target_output,val_input,val_output=read_data(task["data_file"])

    #init time
    begin_time=time.time()

    #init results array
    loss_values=[]
    val_loss_values=[]
    es_values=[0]

    #communicate with scheduler
    try:
        conn.root.start(tid)
    except:
        pass

    #instanciate network 
    if torch.cuda.is_available():
        device=torch.device('cuda')
    else:
        device=torch.device('cpu')
    net=torch.load(task["model_file"],map_location=device)


    #send data to device
    import torch.utils.data as data_utils
    train_data=data_utils.TensorDataset(torch.tensor(target_input,dtype=torch.float,device=device),torch.tensor(target_output,dtype=torch.float,device=device))
    val_input=torch.tensor(val_input,dtype=torch.float,device=device)
    val_output=torch.tensor(val_output,dtype=torch.float,device=device)
    batch_size=task["batch_size"]
    loader_train=data_utils.DataLoader(train_data,batch_size=batch_size,shuffle=True)

    #calculate the checkpoint period
    if task["cp_freq"]==None:
        step=None
    else:
        step=int(task["nb_epochs"]*task["cp_freq"]/100)

    #get loss function
    if isinstance(task["loss"],str):
        criterion=eval("%s()"%(task["loss"]))
    else:
        criterion=task["loss"]

    import torch.optim as optim
    optimizer=eval("optim.%s(net.parameters(),%s)"%(task["optimizer"],task["optim_params"]))

    #initialize the evaluator
    evaluator=task["evaluator"]
    eval_values={}
    for nevl in evaluator.keys():
        eval_values[nevl]=[]

    #initialize the early stopping
    if task["es"]!=None:
        stopper=task["es"](task["es_args"])
    else:
        stopper=None

    #initialize the learning rate adapter
    if task["lra"]!=None:
        target_lra_args=task["lra_args"]
        target_update_lr=task["lra"]
    else:
        target_update_lr=None
        target_lra_args=None
    
    #train the network
    stop=False
    for epoch in range(task["nb_epochs"]):
        for j, (data, labels) in enumerate(loader_train):
            optimizer.zero_grad()
            y_pred=net(data) 
            loss=criterion(y_pred,labels)
            loss_values.append(float(loss))
            y_val_pred=net(val_input)
            val_loss=criterion(y_val_pred,val_output)
            val_loss_values.append(float(val_loss))


            #evaluate
            #print(self.evaluator)
            for nevl,evl in evaluator.items():
                eval_v=evl(net,val_input,val_output,loss_values)
                #print("evaluation with evaluator %s = %s"%(nevl,eval_v))
                eval_values[nevl].append(float(eval_v))
            
            loss.backward() 
            optimizer.step()

            #early stopping
            if stopper!=None: 
                if stopper.testing(eval_values):
                    print("early stopping at epoch %d"%(epoch))
                    stop=True

            #update the leaning rate 
            if target_update_lr!=None:
                lr=target_update_lr(lr,target_lra_args,epoch)

            if step!=None and epoch%step==0:
                completion=100*float(epoch)/float(task["nb_epochs"])
                conn.root.set_completion(tid,completion)
        if stop:
            break

    #save result network 

    #save other results
    res_data_name="%s/%s_res.h5"%(task["results_folder"],tid)
    write_result_file(res_data_name,eval_values,loss_values,val_loss_values)

    #end timer and store result
    end_time=time.time()
    elapsed_time=end_time-begin_time
    etime_str=str(datetime.timedelta(seconds=elapsed_time))
    #print("elapsed time : ",etime_str)

    #stdout & stderr file setting
    stdout_name="%s/%s.stdout"%(task["results_folder"],tid)
    stderr_name="%s/%s.stderr"%(task["results_folder"],tid)

    #build result string
    res_net_name="%s/%s_res.wei"%(task["results_folder"],tid)
    result=dict_serialize({"res_net_name":res_net_name,"res_data_name":res_data_name,"stdout_name":stdout_name,"stderr_name":stderr_name,"etime":etime_str,"last_epoch":es_values[0]})

    #remove all temporary saves
    filelist=glob.glob("%s/%s_checkpoint_*.wei"%(task["results_folder"],tid))
    for f in filelist:
        os.remove(f)

    #communicate with scheduler
    print("training complete for job %s"%(tid))
    conn.root.stop(tid,result)


################################# SERIALIZATION FUNCTIONS ####################

def jupyter_det():
    try:
        a=get_ipython().config
    except:
        return False
    return True

def get_source(f):
    if jupyter_det():
        return inspect.getsource(f)
    else:
        return dill.source.getsource(f)

def serialize_codeobj(f):
    if f==None:
        return None
    sf=get_source(f)
    b_sf=sf.encode('utf8')
    b64_sf=base64.b64encode(b_sf)
    u8_b64_sf=b64_sf.decode('utf8')
    return u8_b64_sf

def deserialize_codeobj(sf):
    if sf==None:
        #print("deserialize none object")
        return None
    b64_df=sf.encode('utf8')
    b_df=base64.b64decode(b64_df)
    df=b_df.decode('utf8')
    #print("df=%s"%(df))
    name=df.split(" ")[1].split("(")[0] 
    #print("extracted name=%s"%(name))
    try:
        print("importing %s"%(name))
        exec(df,vars(__main__))
    except:
        print("unable to instanciate code : ")
        print(df)
        raise
    return  vars(__main__)[name]


def serialize_error(traceback):
    s64=base64.b64encode(traceback.encode('utf8'))
    return s64.decode('utf8')

def deserialize_error(msg):
    ser_b64_b=msg.encode('utf8')
    ser_b=base64.b64decode(ser_b64_b)
    ser_u=ser_b.decode('utf8')
    return ser_u

def unitary_serialization(obj):
    if isinstance(obj,(int,float,str,bool)):
        return obj,"native"
    if isinstance(obj,collections.Callable):
        return serialize_codeobj(obj),"obj"
    if obj is None:
        return "none","none"
    #array recursive serialization
    if isinstance(obj,list):
        val_list=[]
        typ_list=[]
        for e in obj:
            val,typ=unitary_serialization(e)
            val_list.append(val)
            typ_list.append(typ)
        return val_list,typ_list
    #dictionary recursive serialization
    if isinstance(obj,dict):
        val_list={}
        typ_list={}
        for e in obj.keys():
            val,typ=unitary_serialization(obj[e])
            val_list[e]=val
            typ_list[e]=typ
        return val_list,typ_list
    #everything else is pickled
    pickled=codecs.encode(pickle.dumps(obj),"base64").decode()
    return pickled,"pickle"
    #return str(type(obj)),"unknown"
     
def unitary_deserialization(obj,otype,instanciate_objects=True):
    if otype=="native":
        return obj
    if otype=="obj":
        if instanciate_objects:
            return deserialize_codeobj(obj)
        else:
            return None
    if otype=="none":
        return None
    if isinstance(otype,list):
        val_list=[]
        for i in range(len(obj)):
            val=unitary_deserialization(obj[i],otype[i],instanciate_objects=instanciate_objects)
            val_list.append(val)
        return val_list
    if isinstance(otype,dict):
        val_dict={}
        for i in obj.keys():
            val=unitary_deserialization(obj[i],otype[i],instanciate_objects=instanciate_objects)
            val_dict[i]=val
        return val_dict
    if otype=="pickle":
        unpickled=pickle.loads(codecs.decode(obj.encode(),"base64"))
        return unpickled
    print("unknown type : %s"%(type(otype)))

def dict_serialize(d):
    vdict,tdict=unitary_serialization(d)
    serial_params=json.dumps({"values" : vdict , "types" : tdict})
    #print(serial_params)
    s64=base64.b64encode(serial_params.encode('utf8'))
    return s64.decode('utf8')


def dict_deserialize(msg,instanciate_objects=True):
    ser_b64_b=msg.encode('utf8')
    ser_b=base64.b64decode(ser_b64_b)
    ser_u=ser_b.decode('utf8')
    jdict=json.loads(ser_u)
    vdict=jdict["values"]
    tdict=jdict["types"]
    #print(vdict)
    #print(tdict)
    return unitary_deserialization(vdict,tdict,instanciate_objects=instanciate_objects)


def get_paths(desc):
    #decode json dictionary from base64
    dict=dict_deserialize(desc,instanciate_objects=False)
    model_file=dict["model_file"]
    data_file=dict["data_file"]
    results_folder=dict["results_folder"]
    return model_file,data_file,results_folder


#decode('utf8') converts from bytes to utf8
#encode('utf8') converts from utf8 to bytes
    
################################ DATA FUNCTIONS ############################

def read_data(data_file):
    f=h5py.File("%s"%(data_file),"r")
    target_input=f['input'][:]
    #print("input=")
    #print(target_input)
    target_output=f['output'][:]
    #print("output=")
    #print(target_output)
    try:
        val_input=f['input_val'][:]
        #print("input_val=")
        #print(val_input)
    except:
        print("using full input as validation input")
        val_input=target_input
    try:
        val_output=f['output_val'][:]
        #print("output_val=")
        #print(val_output)
    except:
        print("using full output as validation output")
        val_output=target_output
    f.close()
    return target_input,target_output,val_input,val_output

def split_data_set(input_x,input_y,split_pc):
    n=len(input_x)
    val_size=int(n*(split_pc))
    train_size=n-val_size
    train_x=input_x[0:train_size-1]
    train_y=input_y[0:train_size-1]
    val_x=input_x[train_size:]
    val_y=input_y[train_size:]
    return train_x,train_y,val_x,val_y

#temporary
def read_en_data(data_name):
    f=h5py.File("%s/%s"%(data_path,data_name),"r")
    train_set_x,train_set_y=f.get('input'),f.get('output')
    train_set_x,train_set_y=np.array(train_set_x),np.array(train_set_y)
    f.close()
    train_set_x=np.transpose(train_set_x,(2,0,1))
    train_set_y=np.transpose(train_set_y,(1,0))
    x_train=train_set_x[:3000]
    y_train=train_set_y[:3000]
    x_test=train_set_x[3000:]
    y_test=train_set_y[3000:]
    return x_train,y_train,x_test,y_test

def write_data_file(input_data,output_data,filename,input_val=None,output_val=None):
    f=h5py.File(filename,"w")
    f.create_dataset('input',data=input_data)
    f.create_dataset('output',data=output_data)
    if input_val is not None:
        f.create_dataset('input_val',data=input_val)
    if output_val is not None:
        f.create_dataset('output_val',data=output_val)
    f.close()

def write_result_file(filename,eval_values,loss_values,val_loss_values):
    f=h5py.File(filename,"w")
    for k in eval_values.keys():
        f.create_dataset(k,data=eval_values[k])
    f.create_dataset('loss',data=loss_values)
    f.create_dataset('val_loss',data=val_loss_values)
    f.close()





############################### USER FUNCTIONS ############################

def init(scheduler_host):
    newenv={}
    newenv["conn"]=rpyc.connect(scheduler_host,9999)
    newenv["user"]=getpass.getuser()
    newenv["import"]=[]
    #print("in lib : user:%s"%(newenv["user"]))
    return newenv

def importmod(ie,modstr):
    exec("import %s"%(modstr),vars(__main__))
    exec("import %s"%(modstr),globals())
    ie["import"].append(modstr)


def exec_importmod(importmods):
    for m in importmods:
        print("importing %s"%(m))
        exec("import %s"%(m),globals())
        #print(globals())

def get_result(ie,name):
    return dict_deserialize(ie["conn"].root.get_result(name))

def get_eval(res,key):
    filename=res["res_data_name"]
    f=h5py.File(filename,"r")
    eval_values=f[key][:]
    f.close()
    return eval_values

def get_loss(res):
    filename=res["res_data_name"]
    f=h5py.File(filename,"r")
    loss_values=f['loss'][:]
    f.close()
    return loss_values

def get_val_loss(res):
    filename=res["res_data_name"]
    f=h5py.File(filename,"r")
    val_loss_values=f['val_loss'][:]
    f.close()
    return val_loss_values

def print_stdout(res):
    filename=res["stdout_name"]
    f=open(filename,"r")
    for l in f:
        print(l.rstrip())
    f.close()

def print_stderr(res):
    filename=res["stderr_name"]
    f=open(filename,"r")
    for l in f:
        print(l.rstrip())
    f.close()

def plot_eval(res,key):
    eval_values=get_eval(res,key)
    plt.plot(np.arange(len(eval_values)),eval_values,".",label='Evaluator %s values'%(key))
    plt.legend(loc='best')
    plt.show()

def plot_loss(res):
    loss_values=get_loss(res)
    plt.plot(np.arange(len(loss_values)),loss_values,".",label='Loss values')
    plt.legend(loc='best')
    plt.show()

def plot_val_loss(res):
    val_loss_values=get_val_loss(res)
    plt.plot(np.arange(len(val_loss_values)),val_loss_values,".",label='Validation loss values')
    plt.legend(loc='best')
    plt.show()

def dump_model_file(src_filename,dst_filename,framework):
    exec(open("%s"%(src_filename)).read(),globals())
    if framework=="keras":
        return dump_model_keras(target_net,dst_filename)
    if framework=="pytorch":
        return dump_model_pytorch(target_net,dst_filename)
    raise NameError("unknown framework %s (keras,pytorch available)"%(framework))

def dump_model_keras(model,dst_filename):
    model.save(dst_filename)

def dump_model_pytorch(model,filename):
    torch.save(model,filename)

def async_train(ie,name,model_file,data_file,results_folder,nb_epochs,evaluator={},early_stopping=None,es_args=None,cp_freq=5,batch_size=32,lra=None,lra_args=None,seed=1,framework="keras",loss=None,optimizer=None,optim_params=None):
    st=dict_serialize({"model_file":model_file,"data_file":data_file,"results_folder":results_folder,"evaluator":evaluator,"es":early_stopping,"es_args":es_args,"nb_epochs":nb_epochs,"cp_freq":cp_freq,"batch_size":batch_size,"lra":lra,"lra_args":lra_args,"seed":seed,"framework":framework,"loss":loss,"optimizer":optimizer,"optim_params":optim_params,"importmods":ie["import"]})
    ie["conn"].root.submit_task(name,ie["user"],framework,st)

def wait_task(ie,name,silent=0):
    while not ie["conn"].root.finished(name):

        s=ie["conn"].root.status(name)
        if s=="error":
            msg=ie["conn"].root.get_error(name)
            print("\n\n Worker traceback\n")
            print(deserialize_error(msg))
            print("\n\n")
            raise NameError("training failed")

        c=ie["conn"].root.get_completion(name)
        if silent==0:
            progressbar(int(c))
        time.sleep(0.1)
    if silent==0:
        progressbar(100)

def finished_task(ie,name):
    return ie["conn"].root.finished(name)

def ps(ie):
    return ie["conn"].root.ps(ie["user"])

def flushps(ie):
    return ie["conn"].root.flushps(ie["user"])

def all_finished(ie):
    return ie["conn"].root.all_finished(ie["user"])

def get_completion_task(ie,name):
    return ie["conn"].root.get_completion(name)

def get_status_task(ie,name):
    return ie["conn"].root.status(name)
 
def train(ie,name,model_file,data_file,results_folder,nb_epochs,evaluator={},early_stopping=None,es_args=None,cp_freq=5,batch_size=32,lra=None,lra_args=None,silent=0,seed=1,framework="keras",loss=None,optimizer=None,optim_params=None):
    if silent==0:
        print("Submitting the task %s"%(name))
    async_train(ie,name,model_file,data_file,results_folder,nb_epochs,evaluator,early_stopping,es_args,cp_freq,batch_size,lra,lra_args,seed,framework=framework,loss=loss,optimizer=optimizer,optim_params=optim_params)
    wait_task(ie,name,silent=silent)
    return get_result(ie,name)

def progressbar(percent,length=50):
    nb_toprint=int(length*percent//100)
    bar='█'*nb_toprint+'-'*(length-nb_toprint)
    print('\rProgress: |%s| %s%% Completed' % (bar,percent),end='\r')
    if percent==100: 
        print()
    

