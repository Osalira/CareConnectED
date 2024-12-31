// src/utils/csrf.js

/**
 * Retrieves the CSRF token from the browser's cookies.
 * Throws an error if the token is not found.
 *
 * @returns {string} The CSRF token.
 */
// export function getCSRFToken() {
//     const name = 'csrftoken';
//     let cookieValue = null;

//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let cookie of cookies) {
//             cookie = cookie.trim();
//             console.log('Checking cookie:', cookie); // Log each cookie
//             if (cookie.startsWith(`${name}=`)) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     console.log('CSRF Token osa Found:', cookieValue);
//     if (cookieValue === null) {
//         throw new Error('Missing CSRF cookie.');
//     }

//     return cookieValue;
// }
