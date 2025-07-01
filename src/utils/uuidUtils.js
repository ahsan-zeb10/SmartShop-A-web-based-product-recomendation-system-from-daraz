// import { v4 as uuidv4 } from 'uuid';
// import Cookies from 'js-cookie';

// export const getUserUUID = () => {
//   let uuid = Cookies.get('user_uuid') || localStorage.getItem('user_uuid');
//   if (!uuid) {
//     uuid = uuidv4();
//     Cookies.set('user_uuid', uuid, { expires: 365 });
//     localStorage.setItem('user_uuid', uuid);
//   }
//   return uuid;
// };