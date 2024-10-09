import axios from '@/axios'; // Updated import statement

export function login(username, password) {
  return axios.post('/admin/login', {
    username,
    password,
  });
}

export function reg(username, password) {
  return axios.post('/admin/reg', {
    username,
    password,
  });
}
