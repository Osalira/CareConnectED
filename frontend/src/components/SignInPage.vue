<!-- SignInPage.vue -->
<template>
  <div id="app">
    <div class="loginBox">
      <div class="inner">
        <div class="signIn">
          <div class="top">
            <img
              class="logo"
              src="../assets/Logo1.jpeg"
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
          <p v-if="error" class="error">{{ error }}</p>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
      import { useAuthStore } from '../store/auth'

      export default {
      setup() {
          const authStore = useAuthStore()
          return {
          authStore
          }
      },
      data() {
          return {
          employeeId: "", // Renamed for consistency
          password: "",
          error: ""
          }
      },
      computed: {
          loginValid() {
          return this.employeeId && this.password;
          }
      },
      methods: {
          async signIn() {
          try {
              await this.authStore.login(this.employeeId, this.password, this.$router)
              if (!this.authStore.isAuthenticated) {
              this.error = 'Login failed. Please check your credentials.'
              }
          } catch (err) {
              this.error = 'An error occurred during login.'
          }
          },
          resetError() {
          this.error = ""
          }
      }
      }
</script>



<style lang="scss" scoped>

  // Style for the error message
  .error {
    color: red;
    margin-top: 10px;
    font-size: 0.9rem;
    }


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
    width: 290px;
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
    margin-top: 0;
  }
  
  .subtitle {
    .subtitle-action {
      color: rgb(83, 62, 205);
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
    margin-top: 100px;
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