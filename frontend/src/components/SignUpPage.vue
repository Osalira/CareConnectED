<!-- SignUpPage.vue -->
<template>
    <div id="app">
      <div class="loginBox">
        <div class="inner">
          <div class="register">
            <div class="top">
              <img
                class="logo"
                src="https://www.mistered.de/MisterEDk.png"
              />
              <div class="title">Create an Account</div>
              <div class="subtitle">
                Already have an account?
                <router-link class="subtitle-action" to="/">
                  Sign In
                </router-link>
              </div>
            </div>
  
            <form @submit.prevent="signUp">
              <div class="form">
                <input
                  type="text"
                  placeholder="First Name"
                  v-model="firstName"
                  class="w100"
                  required
                />
                <input
                  type="text"
                  placeholder="Last Name"
                  v-model="lastName"
                  class="w100"
                  required
                />
                <input
                  type="text"
                  placeholder="Employee ID"
                  v-model="employeeId"
                  class="w100"
                  required
                />
                <input
                  type="password"
                  placeholder="Password"
                  v-model="password"
                  class="w100"
                  required
                />
              </div>
  
              <button type="submit" class="action" :disabled="!registerValid">
                Create Account
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
</template>
  
<script>
import { getCSRFToken } from '../store/auth'

export default {
  data() {
    return {
      firstName: '',
      lastName: '',
      employeeId: '',
      password: '',
      error: '',
      success: ''
    }
  },
  computed: {
    registerValid() {
      return this.firstName && this.lastName && this.employeeId && this.password;
    }
  },
  methods: {
    async signUp() {
      try {
        const response = await fetch('http://localhost:8001/api/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
          },
          body: JSON.stringify({
            first_name: this.firstName,  // Add first_name
            last_name: this.lastName, // Add last_name
            employee_id: this.employeeId,
            password: this.password
                 
          }),
          credentials: 'include'
        });
        const data = await response.json();
        if (response.ok) {
          this.success = 'Registration successful! Please log in.';
          setTimeout(() => {
            this.$router.push('/signin');
          }, 500);
        } else {
          this.error = data.error || 'Registration failed';
        }
      } catch (err) {
        this.error = 'An error occurred during registration: ' + err;
      }
    }
  }
}
</script>

  
<style lang="scss" scoped>

  html, body, #app {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0;
  }

  @mixin box {
    box-shadow: 1px 1px 2px 1px #ccc;
  }
  
  @mixin field {
    border: 1px solid #aaa;
    height: 40px;
    padding: 10px;
    margin-top: 20px;
    border-radius: 5px;
    box-sizing: border-box;
  }
  
  input[type="text"],
  input[type="password"] {
    @include field;
  }
  
  .invalid {
    border: 2px solid red !important;
    &::placeholder {
      color: red;
    }
  }
  
  .w100 {
    width: 100%;
  }
  
  .logo {
    width: 300px;
    margin-bottom: 10px;
  }
  
  .action {
    height: 40px;
    text-transform: uppercase;
    border-radius: 25px;
    width: 100%;
    border: none;
    cursor: pointer;
    background: green;
    margin-top: 20px;
    color: #fff;
    font-size: 1.2rem;
    @include box;
  }
  
  .action:disabled {
    background: #aaa;
    cursor: not-allowed;
  }
  
  .top {
    display: flex;
    align-items: center;
    flex-direction: column;
    margin-bottom: 10px;
  }
  
  .title {
    width: 100%;
    font-size: 1.8rem;
    margin-bottom: 10px;
    text-align: center;
  }
  
  .subtitle {
    .subtitle-action {
      color: green;
      font-weight: bold;
      cursor: pointer;
    }
  }
  
  html {
    background-repeat: no-repeat;
    background: linear-gradient(
      to bottom,
      rgba(96, 108, 136, 1) 0%,
      rgba(63, 76, 107, 1) 100%
    );
    background-size: cover;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    font-family: sans-serif;
  }
  
  .loginBox {
    background: #fff;
    border-radius: 15px;
    max-width: 400px;
    padding: 25px 55px;
    margin-top: 50px;
    animation: slideInTop 1s;
  }
  
  @keyframes slideInTop {
    from {
      opacity: 0;
      transform: translateY(-30%);
    }
  
    to {
      opacity: 100;
      transform: translateY(0%);
    }
  }
  
  @media screen and (min-width: 440px) {
    .loginBox {
      @include box;
    }
  }
  
  @media screen and (max-width: 440px) {
    html {
      background: #fff;
      align-items: start;
      justify-content: start;
    }
  
    .loginBox {
      padding: 25px 25px;
      max-width: 100vw;
    }
  }
</style>
  