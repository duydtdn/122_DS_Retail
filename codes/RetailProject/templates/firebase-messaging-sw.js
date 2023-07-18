importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing in
// your app's Firebase config object.
// https://firebase.google.com/docs/web/setup#config-object
firebase.initializeApp({
  apiKey: "AIzaSyBIdQ_8-YwVcpwNqPmwrvmIKGQDI3sG-n8",
  authDomain: "retail-project-148d8.firebaseapp.com",
  projectId: "retail-project-148d8",
  storageBucket: "retail-project-148d8.appspot.com",
  messagingSenderId: "207411045636",
  appId: "1:207411045636:web:bbb1687ea92b8e04569c51",
  measurementId: "G-LG0GLDWVQJ"
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();

// messaging.onMessage((payload) => {
//   console.log('Message received. ', payload);
//   // ...
// });
messaging.onBackgroundMessage((payload) => {
  console.log(
    '[firebase-messaging-sw.js] Received background message ',
    payload
  );
  // Customize notification here
  const notificationTitle = 'New order receive';
  const notificationOptions = {
    body: 'Your store have a new order.',
    icon: '/firebase-logo.png'
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});