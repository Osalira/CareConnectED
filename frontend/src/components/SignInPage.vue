<!-- SignInPage.vue -->
<template>
    <div id="app">
      <div class="loginBox">
        <div class="inner">
          <div class="signIn">
            <div class="top">
              <img
                class="logo"
                src="https://www.mistered.de/MisterEDk.png"
              />
              <div class="title">Sign In</div>
              <div class="subtitle">
                Don't have an account?
                <router-link class="subtitle-action" to="/signup">
                  Create Account
                </router-link>
              </div>
            </div>
            <form @submit.prevent="signIn">
              <div class="form">
                <input
                  required
                  aria-required="true"
                  aria-label="Employee ID"
                  type="text"
                  class="w100"
                  placeholder="Employee ID"
                  v-model="employeeId"
                />
                <input
                  required
                  aria-required="true"
                  type="password"
                  class="w100"
                  placeholder="Password"
                  v-model="password"
                />
              </div>
              <button type="submit" class="action" :disabled="!loginValid">Sign In</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        employeeId: '',
        password: '',
      };
    },
    methods: {
      async signIn() {
        try {
          const response = await axios.post('/api/auth/jwt/create/', {
            employee_id: this.employeeId,
            password: this.password,
          });
          const { access } = response.data;
          localStorage.setItem('token', access);
          await this.getEmployeeDetails();
          this.$router.push('/');
        } catch (error) {
          console.error('Error during sign-in:', error);
          alert('Invalid credentials.');
        }
      },
      async getEmployeeDetails() {
        const token = localStorage.getItem('token');
        const response = await axios.get('/api/auth/users/me/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const { first_name, last_name } = response.data;
        localStorage.setItem('employeeName', `${first_name} ${last_name}`);
      },
    },
    computed: {
      loginValid() {
        return this.employeeId && this.password;
      },
    },
  };
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
  
  input[type="text"] {
    @include field;
  }
  
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
    margin-top: 120px;
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
  