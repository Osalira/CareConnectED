<!-- SignUpPage.vue -->

<template>
  <div id="app">
    <div class="loginBox">
      <div class="inner">
        <div class="register">
          <div class="top">
            <img class="logo" src="/assets/logo1.jpeg" alt="Logo" />
            <div class="title">Create an Account</div>
            <div class="subtitle">
              Already have an account?
              <router-link class="subtitle-action" to="/">Sign In</router-link>
            </div>
          </div>

          <!-- Display error message -->
          <div v-if="error" class="error-message">
            {{ error }}
          </div>

          <form @submit.prevent="signUp">
            <div class="form">
              <label for="firstName">First Name</label>
              <input
                id="firstName"
                type="text"
                placeholder="First Name"
                v-model="firstName"
                class="w100"
                required
              />

              <label for="lastName">Last Name</label>
              <input
                id="lastName"
                type="text"
                placeholder="Last Name"
                v-model="lastName"
                class="w100"
                required
              />

              <label for="employeeId">Employee ID</label>
              <input
                id="employeeId"
                type="text" 
                placeholder="Employee ID"
                v-model="employeeId"
                class="w100"
                required
              />

              <label for="password">Password</label>
              <input
                id="password"
                type="password"
                placeholder="Password"
                v-model="password"
                class="w100"
                required
              />

              <label for="confirmPassword">Confirm Password</label>
              <input
                id="confirmPassword"
                type="password"
                placeholder="Confirm Password"
                v-model="confirmPassword"
                class="w100"
                required
              />
            </div>

            <button
              type="submit"
              class="action"
              :disabled="!registerValid || isLoading"
            >
              <span v-if="isLoading">Creating Account...</span>
              <span v-else>Create Account</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/store/auth';
import Swal from 'sweetalert2';

export default {
  setup() {
    const authStore = useAuthStore();
    return {
      authStore,
    };
  },
  data() {
    return {
      firstName: '',
      lastName: '',
      employeeId: '',
      password: '',
      confirmPassword: '',
      error: '',
      isLoading: false, // Loading state
    };
  },
  computed: {
    registerValid() {
      return (
        this.firstName &&
        this.lastName &&
        this.employeeId &&
        this.password &&
        this.confirmPassword &&
        this.password === this.confirmPassword
      );
    },
  },
  methods: {
    async signUp() {
      if (this.password !== this.confirmPassword) {
        this.error = 'Passwords do not match!';
        setTimeout(() => (this.error = ''), 3000);
        return;
      }

      this.isLoading = true;

      try {
        await this.authStore.register({
          first_name: this.firstName,
          last_name: this.lastName,
          employee_id: this.employeeId,
          password: this.password,
        });

        // SweetAlert success popup
        await Swal.fire({
          title: 'Account Created Successfully!',
          text: 'Please sign in with your new credentials.',
          icon: 'success',
          confirmButtonText: 'OK',
          background: '#f0f8ff',
          confirmButtonColor: '#4CAF50',
          iconColor: '#4CAF50',
        });

        this.$router.push({ name: 'WelcomePage' });
      } catch (err) {
        this.error = 'An error occurred during registration.';
      } finally {
        this.isLoading = false;
      }
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
    margin-bottom: 20px;
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
  width: 290px;
  margin-bottom: 0; 
}
  
  .action {
    height: 40px;
    text-transform: uppercase;
    border-radius: 25px;
    width: 100%;
    border: none;
    cursor: pointer;
    background: rgb(18, 171, 99);
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
  margin-bottom: 0; /* Remove bottom margin */
  padding-top: 10px; /* Reduce gap between logo and top of sign-in box */
}
.title {
  width: 100%;
  font-size: 1.8rem;
  margin: 0; /* Remove all margins to eliminate any gap */
  text-align: center;
  padding-top: 10px; /* Add a little padding for spacing if needed */
}
  
  .subtitle {
    .subtitle-action {
      color: rgb(55, 45, 196);
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
      max-height: 600px;
    }
  }

.error-message {
  color: red;
  margin-top: 10px;
  text-align: center;
}

.action:disabled {
  background: #aaa;
  cursor: not-allowed;
}

.form label {
  display: block; /* Ensures the label is above the input */
  margin-top: 10px;
  margin-bottom: 5px; /* Reduces space between label and input */
  font-weight: bold; /* Optional: Makes the label stand out */
}

.form input {
  margin-top: 0; /* Removes unnecessary top margin from input */
}

</style>
  