// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getStorage } from "firebase/storage";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyA6ZWJb3_CzezS_-usFVDyny6jzcVUrLAo",
  authDomain: "igcse-predict.firebaseapp.com",
  projectId: "igcse-predict",
  storageBucket: "igcse-predict.appspot.com",
  messagingSenderId: "876468127148",
  appId: "1:876468127148:web:efc70cc475d92b12d3e609",
  measurementId: "G-WWB1WB30CG",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

export default storage;
