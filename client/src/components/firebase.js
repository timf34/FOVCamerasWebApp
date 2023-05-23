// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyA5bTqNoQwo2enAjRYTuULwIgsUVY2DGO0",
  databaseURL: "https://fov-cameras-web-app-default-rtdb.europe-west1.firebasedatabase.app",
  authDomain: "fov-cameras-web-app.firebaseapp.com",
  projectId: "fov-cameras-web-app",
  storageBucket: "fov-cameras-web-app.appspot.com",
  messagingSenderId: "482731723458",
  appId: "1:482731723458:web:eea5f59b23da8a544d895b"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Auth
const auth = getAuth();

export { auth };
