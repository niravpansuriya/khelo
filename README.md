# Khelo

- This is an Audio QR based Attendance System.
- There are many ways to make an attendance system fast in schools and colleges i.e. To take attendance with the help of QR Code. But this is very insecure as many students can do fake proxies, just by sending the QR code to his/her friend.
- So, We have come with a unique idea to make an Attendance System very fast, reliable, and extremely secure.
- We have used Chirp.io. Chirp is an API that can transfer the data over sound.
 

### How it works?

- There two mobile applications - Present Me (for students) and Present Me Pro (for professors).
- There is one web portal.
- Now admin can use the web portal to add a person and assign them roles (student or professor) manually or by just uploading the CSV file.
- Now a professor has to install the Present Me Pro application and login with their credentials.
- Students have to install the Present Me application and login with their credentials.
- Now, Professor will add lecture details and these details are sent to the server.
- By encrypting these details, the server gives a token to the Present Me Pro application, which will transfer that token with the help of Chirp.
- Students have to just keep open the Present Me application.
- Present Me application receives the sound and chirp convert it into the token (the one which was given by the server to professor) again.
- This token is sent to the server with student info.
- The server checks the information of the student. And then token decrypted by the server.
- And with this, attendance of the student marked into a system by the server.


### Advantages

- Chirp generates a very high pitch sound, which is enough to be received from any corner of the normal classroom. So, in just 8-10 seconds, the whole classroom's attendance (around 90-100 students') can be done by this system.
- This attendance can be managed very easily by the professor in the web portal.
- This is system is highly scalable and very secure.
- Professor can also mark attendance manually in the web portal, in case any student forgot the cell phone at home.


### Why this is so secure?

- Only the admin can add students and professors in the system. Only an admin can change or generate the password.
- When the first-time student login in the android device with his/her credentials, the IMEI number of this device stored in the database. (Admin can not see it and system encrypt it before storing). So, after the first login, the student does not need to log in every time.
- Now suppose any student tries to login with any other student's credentials, with the help of IMEI number both will be blocked by the system.
- Only admin can unblock any blocked student.
- If any student purchases a new device, only the admin can add him/her to the system.
- PresentMe application needs the fingerprint of the student in the android device to open the application.
- We have signed our android applications and we are sending a signed key with the package and check it on the server. So, if someone tries to do reverse engineering and rebuild the application, the system will detect it and block them in the system.
- We have used ProGuard, so reverse engineering is very difficult. Other than this, we have encrypted variable names. This makes reverse engineering extremely tough.
- Token used for mark attendance is encrypted by timestamp. So, students do not have time to record the audio and send it to another student to mark the fake attendance.
- **Because we have encrypted variable names, code looks dirty.**


### Build with

- [Java](https://www.java.com/en/)
- [Chirp](https://github.com/chirp) - API for transfer data with sound
- [mysql](https://www.mysql.com/) - Database
- [Hibernate](https://hibernate.org/) - Java framework for simplifies application to interect with database
- [Spring](https://spring.io/) - Java Application Development Framework


### Demo

- Watch a [demo](https://github.com/niravpansuriya/khelo/blob/master/demo.mp4)


## Authors

* **Nirav C. Pansuriya**
* **Smit H. Parmar**
* **Brij S. Patel**
* **Anuj H. Patel** 
