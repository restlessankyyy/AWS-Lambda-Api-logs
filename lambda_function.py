import boto3
def lambda_handler(event, context):
    print event
    try:
        eventname=event['detail']['eventName']
    except Exception :
        eventname=event['eventName']
    msg= "Hi \n\n"
    msg=msg+ "New Resource provisioned in your AWS account \n"
    if eventname=='CreateBucket':
        tagdet=['first','sec'] # tag filter checklist
        s3client = boto3.client('s3')
        #print eventname
        buc_name=event['detail']['requestParameters']['bucketName']
        msg=msg+ "Resource Type: " + "S3 Bucket \n"
        msg=msg+ "Resource Name: " + str(buc_name) + "\n\n"
        try:
            resrs3tag = s3client.get_bucket_tagging(
                   Bucket=buc_name
                                )
            res=tag_check(tagdet,resrs3tag['TagSet'])
        except Exception:
            res="Tag Check Result: \n"
            res=res+ "No tags found\n"
        msg=msg+res    
        msg=msg+ "\nThanks"
        calltosns(msg)
    else:
        try:
            eventsrc=event['source'].split('.')[1]
        except Exception:
            eventsrc=event['eventSource'].split('.')[0]
        msg=msg+ "Resource Type: " + str(eventsrc)+" \n"
        reqparam=event['detail']['requestParameters'].keys()
        #print reqparam
        res_name=''
        for key in reqparam:
            kname=str(key)
            #print kname
            #print kname.find('Name')
            if kname.find('Name')>=0:
                #print kname# + "Findddd"
                res_name=event['detail']['requestParameters'][kname]
        if res_name!='':
            msg=msg+ "Resource Name: " + str(res_name) + "\n"
            msg=msg+ "Event Name: " + str(eventname) + "\n\n"
        else:
            msg=msg+ "Event Name: " + str(eventname) + "\n\n"
        
        msg=msg+ "\nThanks"
    print msg
    calltosns(msg)
def calltosns(msg):
    sub="Notification for Resource Provisioning (AWS)"
    sns = boto3.client('sns')
    sns.publish(
                  TopicArn='arn:aws:sns:ap-south-1:107840965488:send_notif', # SNS topic ARN 
                  Message=msg,
                  MessageStructure='string',
                  Subject=sub,
                  MessageAttributes={
                       'summary': {
                              'StringValue': 'Sending Notification',
                              'DataType': 'String'
                       }
                  }
            )
def tag_check(tagdet,tagpre):
    taglen=len(tagdet)
    print tagpre
    keylist=list()
    #print resrs3tag['TagSet'][0].values()
    for j in range(len(tagpre)):
        keylist.append(tagpre[j].values()[1])
    msg= "Tag Check Result: \n"    
    print keylist   
    f=0
    for i in range(len(tagdet)):
        #print resrs3tag['TagSet']
        if tagdet[i] in keylist:
            print str(tagdet[i]) + " Is present"
        else:
            f=1
            msg= msg+ str(tagdet[i]) + " Is not present \n"
            #print str(tagdet[i]) + " Is not present"
    if f==0:
        msg=msg+ "All tag is present \n"
    return msg