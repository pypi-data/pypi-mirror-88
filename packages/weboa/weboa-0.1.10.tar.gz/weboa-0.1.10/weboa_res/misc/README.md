>>> Change ToDo:
1. php/configs/(en|*).php
2. php/db.php
3. /favicon.ico/
4. /img/favicon.png
5. /img/sn_share.png

----  

## Nginx config  
```
location / {  
     try_files $uri $uri/ /index.php?$args;  
}  
```