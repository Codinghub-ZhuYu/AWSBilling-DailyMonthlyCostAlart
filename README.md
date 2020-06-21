# AWSBilling-DailyMonthlyCostAlart
This project will let you send alart based on your customized value of daily cost and monthly cost in AWS China region, but it will smoothly be applied to AWS GLB resion with very low effort.

Background:
Customer want to know their potential burst cost as soon as possible to lower the risk to pay a great amount of money at the billing time. AWS internal employees should also pay attention on their cost on AWS resource during the POC. But AWS has no good way to have alert on a daily and monthly (the same day cost last month vs current cost till today) basis. This solutions will give alert notification to account owners the potential risk according to the customized value such as the max money they can afford for one day and the monthl growth rate.
Pre-request:
1.	Have a china region account
2.	Enable AWS billing alert – how to do it visit this link 
3.	Have Full admin right in the account to set the alert notification 

Overview of all the component in cloud formation template:
 
We have below components:
1.	An event rule to trigger lambda function for cost evaluation.
2.	Lambda function which have cloud watch, SNS access rights to get cost data from cloudwatch and publish notification for the alerts.
3.	SNS topic with email subscription to it to get the alert notification.
4.	Lambda function code which is zipped with the name “BillingAlertCode.zip”, you need to upload it to your S3 bucket in the same region with your lambda function.
5.	A cloud formation template file to automatically set all above automatically

Deploy Steps:
1.	Upload the code zip to your S3 bucket – record the bucket name and the object key name
  bucketName:  “billingalert”, object key name: “BillingAlertCode.zip”
2.	Create a new stack with proper information
  •	Go to cloud formation and create a stack using template
  •	Click “create template in the designer” and copy the CloudFormation.json content to the designer and then validate and create stack:
  •	Choose next
  •	Input the right parameters 
  •	Choose all default options to the end of the wizard. It takes 3 minutes to finish all the creation work.
3.	Confirm the subscription from your email
4.	Now you are in good shape to get notification when abnormal cost happens.
5.	If you want to know detailed cost information you could go to lambda log as below
 





