from flask import Flask, request
import boto3
import os

app = Flask(__name__)

region = 'ap-south-1'
ec2 = boto3.resource('ec2', region_name='us-west-2', aws_access_key_id=os.environ.get(
    'AWS_SERVER_PUBLIC_KEY'), aws_secret_access_key=os.environ.get('AWS_SERVER_SECRET_KEY'))


@app.route('/tool', methods=['POST'])
def tool():
    action = request.args.get('action')
    if action.notnull():
        turn_on_instance_list = []
        turn_off_instance_list = []

        for instance in ec2.instances.all():

            increment = 0
            for tags in instance.tags:

                # Used to get the Key and Value from the EC2 instance tags using Boto3.
               # if tags['Key'] == 'Automatic Schedule' or tags['Key'] == 'automatic schedule':
               #     schedule_flag = instance.tags[increment]['Value']
                if tags['Key'] == 'Turn On' or tags['Key'] == 'turn on':
                    turn_on_flag = instance.tags[increment]['Value']
                if tags['Key'] == 'Turn Off' or tags['Key'] == 'turn off':
                    turn_off_flag = instance.tags[increment]['Value']

                increment = increment + 1

                # Validates if EC2 requires 'Instance Start' and 'Instance Stop' by comparisson and collects EC2 instance ID.
               # if schedule_flag == 'Enabled' or schedule_flag == 'enabled':
                # if str(current_time) == str(turn_on_flag):

                if action == 'start':
                    instance_id = instance.id
                    turn_on_instance_list.append(instance_id)
                    return "Turned on or off EC2 Instances"
                elif action == 'stop':
                    instance_id = instance.id
                    turn_off_instance_list.append(instance_id)
                    return "Turned on or off EC2 Instances"

                else:

                    return "No EC2 Instances to start or stop"
                schedule_flag = ""
                turn_on_flag = ""
                turn_off_flag = ""

        if turn_on_instance_list == [] and turn_off_instance_list == []:
            return "No EC2 Instances to start or stop"

        # Triggers the Lambda_handler, passes EC2 instance ID and executes Instance_state operation.
        ec2 = boto3.client('ec2', region_name=region)

        def lambda_handler(event, context):

            if turn_on_instance_list != []:
                ec2.start_instances(InstanceIds=turn_on_instance_list)
                print('EC2 Instances have been started: ' +
                      str(turn_on_instance_list))
                return "EC2 Instances have been started: " + str(turn_on_instance_list)

            if turn_off_instance_list != []:
                ec2.stop_instances(InstanceIds=turn_off_instance_list)
                print('EC2 Instances have been stopped: ' +
                      str(turn_off_instance_list))
                return "EC2 Instances have been stopped: " + str(turn_off_instance_list)

            turn_on_instance_list.clear()
            turn_off_instance_list.clear()
            exit()


app.run(port=5000)
