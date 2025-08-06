# Irrigation Tool Hub Application
This repository contains a Python implementation of the Crop Water Stress Index (CWSI) calculation along with the WISE tool, deployed on Azure, using Flask. The WISE calculation is from the following paper:
[Andales et al 2014 AASM mobileIWM.pdf](https://github.com/user-attachments/files/21639830/Andales.et.al.2014.AASM.mobileIWM.pdf)

Follow the instructions below to set up using Microsoft Azure.

Requirements:
- Microsoft Azure Account

---------------------------------
### Create a Fork of the Repository:

<img width="875" height="525" alt="Screenshot from 2025-08-06 12-00-49" src="https://github.com/user-attachments/assets/978729cf-0d39-4ce3-bd80-b14b0ce33f80" />

<img width="882" height="691" alt="Screenshot from 2025-08-06 12-01-31" src="https://github.com/user-attachments/assets/e18f6b7b-d193-4967-8073-623391a90e30" />

---------------------------------
### Next Delete the Workflow File
Click on “.github/workflows” folder then click on the .yml file

<img width="878" height="635" alt="Screenshot from 2025-08-06 12-13-06" src="https://github.com/user-attachments/assets/b077140c-eafd-4c8c-b8f1-76cc25889425" />

Select the three dots icon and delete the file, commit the changes

<img width="881" height="696" alt="Screenshot from 2025-08-06 13-44-25" src="https://github.com/user-attachments/assets/baf44f54-6aac-4d33-b4d8-e73870d88e14" />

The repository should now look like this:

<img width="881" height="696" alt="Screenshot from 2025-08-06 13-45-55" src="https://github.com/user-attachments/assets/23f5413b-35a3-4896-84fe-1c1fbe524bb1" />

---------------------------------
### Go to your Microsoft Azure Account, Create the App
You should see this on the home page, click on "Create a resource"

<img width="828" height="353" alt="Screenshot from 2025-08-06 11-13-02" src="https://github.com/user-attachments/assets/3c5d8a36-9d92-46b9-9fc5-24dc2ae03b5f" />

Click, "create" next to the Web App icon

<img width="739" height="663" alt="Screenshot from 2025-08-06 11-14-05" src="https://github.com/user-attachments/assets/c3ed198f-356c-412a-b010-9e83ec8e5197" />

App creation settings:
- Choose a name
- For publish model select “Code”
- Runtime stack is python 3.12
- Region defaults to Canada, select Central US
- For pricing plan, select Free F1 (or Basic B1 if its too slow)
- Ignore Database and deployment Tab
- For Networking tab, enable public access on
- Monitor+secure: no application insights or defender
- Ignore Tags
- Review+create: Make sure everything looks right, then create

<img width="1218" height="963" alt="Screenshot from 2025-08-06 11-11-54" src="https://github.com/user-attachments/assets/50b7c0ea-ee2f-4d02-ab5b-a7cc8768b38f" />

On the Azure home page, you should now see the App Service resource you just created. Click on the name.

<img width="897" height="589" alt="Screenshot from 2025-08-06 11-34-08" src="https://github.com/user-attachments/assets/d2fcc48d-2584-4f65-8c9c-9195e451290e" />

On the side bar, go to “Deployment”, and under that tab should be “Deployment Center.”

<img width="499" height="706" alt="Screenshot from 2025-08-06 11-38-03" src="https://github.com/user-attachments/assets/0523aa55-d81d-4c69-8888-34d10df3a517" />

Then, for code source, select “GitHub.” Under the GitHub tab, sign in using your github account that has the forked repository

<img width="1168" height="882" alt="Screenshot from 2025-08-06 11-54-34" src="https://github.com/user-attachments/assets/7edaab32-c8af-4aef-bd2c-09a6a73a9989" />

<img width="561" height="518" alt="Screenshot from 2025-08-06 12-11-10" src="https://github.com/user-attachments/assets/7eef82d0-8ad9-4779-858b-00ee9a118031" />

Add a workflow, select your subscription and the Identity box, then scroll to the top and save

<img width="614" height="889" alt="Screenshot from 2025-08-06 13-48-55" src="https://github.com/user-attachments/assets/af061d65-a328-42cd-9672-4e9b6e6bba03" />

---------------------------------
### Final Setup Steps

Return to your repository, which should now have a workflow
<img width="591" height="517" alt="Screenshot from 2025-08-06 13-51-12" src="https://github.com/user-attachments/assets/fee77cd8-8e02-4927-aba9-d528aa799102" />

If you go to the Actions tab, you will see it deploying. Wait until it's done.

<img width="871" height="402" alt="Screenshot from 2025-08-06 13-52-09" src="https://github.com/user-attachments/assets/8438c399-f73f-40e5-b421-a63ccf04ebb3" />

<img width="871" height="402" alt="Screenshot from 2025-08-06 13-57-05" src="https://github.com/user-attachments/assets/a9654c76-69b1-4f47-aea3-467623647ade" />

Now, go to “Overview” on the side bar in Azure, and click the link under “Default domain”

<img width="960" height="720" alt="Screenshot Thing" src="https://github.com/user-attachments/assets/cf59bbeb-6025-498a-b6d3-c6495d9a7d9b" />

This links to the website, which will automatically be updated when you commit to your repository

![image](https://github.com/user-attachments/assets/75601f0d-092b-4745-b07b-91909b3f1144)




