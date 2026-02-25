const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const emailerr = document.getElementById('emailError')
const pwerr = document.getElementById('passwordError')

const make_post = (email, pw) => {
   const data = {
      email: email,
      password: pw
   }

   fetch('/form', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
   }).then(resp => {
      if (!resp.ok) throw new Error('Response Fault')
      return resp.json()
   }).then(result => {
      console.log('Success:', result)
   }).catch(err => {
      console.error('Error:', err)
   })
}

document.getElementById('formData').addEventListener('submit', async (e) => {
   const email = document.getElementById('email').value;
   const password = document.getElementById('password').value;
   
   e.preventDefault()
   let isValid = true;

   if (!emailRegex.test(email)) {
      emailerr.textContent = 'Invalid email format';
      isValid = false;
   } else {
      emailerr.textContent = '';
   }

   if (password.length < 8) {
      pwerr.textContent = 'Password must be at least 8 characters';
      isValid = false;
   } else {
      pwerr.textContent = '';
   }

   if (isValid) {
      make_post(email, password)
      // You can proceed with actual form submission here, e.g., using fetch()
   }
});
