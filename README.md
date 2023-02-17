# GCP_Auditlogs

This project explores the issue of **data governance(DG)** and focus on the topic of **Cloud Monitoring & Logging** to control the abnormal behavior of the users.


## Research Background

<img width="700" alt="截圖 2023-02-02 上午10 56 06" src="https://user-images.githubusercontent.com/92499570/216220121-d3cec028-e94e-4780-b30e-e49c4938f20e.png">

## Commands to run

**1.** Download the folder and verify your `project_id`, `dataset_id`, and `sender/receiver email`

**2.** If you don't have app passwords, generate it first! [Sign in to your account with your app password ](https://support-google-com.translate.goog/accounts/answer/185833?hl=zh-Hant&_x_tr_sl=zh-TW&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=sc )

**3.** Create your Cloud Run service in your project [Cloud Run overview ]( https://cloud.google.com/run/docs/overview/what-is-cloud-run)

<img width="800" alt="截圖 2023-02-17 上午9 36 55" src="https://user-images.githubusercontent.com/92499570/219527340-0a4a1bc8-8ab0-44c2-b01c-791a2e3fc3a9.png">


Then you can run the command below to build using Dockerfile and deploy container to your Cloud Run service in your project.  

>`gcloud run deploy YourServiceName --source .`  


## Result
<img width="294" alt="截圖 2023-02-10 下午4 49 18" src="https://user-images.githubusercontent.com/92499570/218046082-a2b12b2a-f40f-4df7-bd02-6541b60d8cf0.png">

<img width="270" alt="截圖 2023-02-17 上午9 26 13" src="https://user-images.githubusercontent.com/92499570/219525957-d2ccf830-1b3e-4760-bf7f-1fd59a39a0f4.png">
