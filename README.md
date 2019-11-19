# innerproduct
A simple API server developed for interview.
 
 ### Paths
   * /innerProduct - 目前只允許使用 POST 訪問，使用者輸入兩個 array ，若符合格式限制則回傳兩個 array 進行內積後的結果。
   * /info - 目前只允許使用 GET 訪問，管理者可透過此路徑獲取目前 /innerProduct 被 request 的統計狀況，包含總 request 次數及 error 次數。

 ### Other methods
   * checkArray(xArray,yArray) - 用來確認使用者輸入的 array 是否符合相關的格式規定 (兩個 array 長度需相同，且介於 1~50 之間，此外內容僅包含 integer)。
   * innProduct(xArray,yArray) - 用來計算兩個 array 的內積結果。
    
 ### Server
    Flask - 一種輕量級的 python web framework。

 ### Requirements
   * requests - 處理 request 的資料。
   * datetime - 用來記錄 request 的時間。
   * flask-pymongo - MongoDB 的 driver，用來與 DB 建立連結及處理相關指令。
    
 ### Database
    MongoDB
    
 ### Deployment
    目前架設在 Heroku 上，路徑為: https://intense-everglades-52145.herokuapp.com/
    資料庫部分則是利用 Heroku 所提供的 add-on: mLab MongoDB 來提供服務。
    可於 Heroku 提供的後台管理處設定相關的環境變數(如:相關 config 設定、DB連接路徑)，並在 github 的 repo 更新後，可於此介面選擇相關的 branch 來進行 新版本的 deployment。
    另外，可於 mLab 的相關管理介面來觀看 DB 的資料儲存狀況並進行基本管理，但如果是較複雜的操作建議還是利用 mongo 指令來連接相關的資料庫進行。

 ### Todo
   目前可能由於架設的主機皆在歐美，故 response time 不如預期，下一步的首要改善目標即是加快 response time。

   另外，Heroku 本身有提供 CI/CD 功能，這點也是接下來可以加強的方向。