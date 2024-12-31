<template>
    <div class="modal fade show" tabindex="-1" style="display: block;" aria-modal="true" role="dialog">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Reschedule Appointment</h5>
            <button type="button" class="btn-close" aria-label="Close" @click="$emit('close')"></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="new-time" class="form-label">New Date & Time</label>
                <input
                  id="new-time"
                  type="datetime-local"
                  class="form-control"
                  v-model="newTime"
                />
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="reschedule">Submit</button>
            <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Swal from 'sweetalert2';
  
  export default {
    props: {
      appointment: {
        type: Object,
        required: true,
        default: () => ({}),
      },
    },
    data() {
      return {
        newTime: '',
      };
    },
    methods: {
      async reschedule() {
        try {
          if (!this.appointment.id) {
            console.error('Missing appointment ID');
            return;
          }
          await this.$axios.patch(`/appointments/${this.appointment.id}/reschedule/`, {
            scheduled_time: this.newTime,
          });
          Swal.fire({
            icon: 'success',
            title: 'Appointment Rescheduled',
            text: 'The appointment has been successfully rescheduled!',
          });
          this.$emit('close');
          this.$emit('refresh');
        } catch (error) {
          console.error('Error rescheduling appointment:', error);
          Swal.fire({
            icon: 'error',
            title: 'Failed to Reschedule',
            text: 'An error occurred while rescheduling. Please try again.',
          });
        }
      },
    },
  };
  </script>  
  
  <style scoped>
  .modal-backdrop {
    background: rgba(0, 0, 0, 0.5);
  }
  </style>
  
  