// src/api/manager.js
import { auth, db } from '@/firebase';
import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from 'firebase/auth';
import { doc, setDoc } from 'firebase/firestore';

export async function register(email, password, name, role) {
  const userCredential = await createUserWithEmailAndPassword(auth, email, password);
  const user = userCredential.user;

  // Save additional user data to Firestore
  await setDoc(doc(db, "Users", user.uid), {
    UID: user.uid,
    email,
    name,
    role,
  });

  return user;
}

export async function login(email, password) {
  return await signInWithEmailAndPassword(auth, email, password);
}
