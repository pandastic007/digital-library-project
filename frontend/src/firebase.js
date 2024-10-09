// src/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyBvfuYK-UPc5nUnh6UxItEOQ16LNjGnCis",
  authDomain: "digital-library-aea91.firebaseapp.com",
  projectId: "digital-library-aea91",
  storageBucket: "digital-library-aea91.appspot.com",
  messagingSenderId: "996184561285",
  appId: "1:996184561285:web:0a76fa6f9397451c407bec",
  measurementId: "G-90XN4MEFXN"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { auth, db };
