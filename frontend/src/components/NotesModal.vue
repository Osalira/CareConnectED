<template>
    <div class="modal fade show" tabindex="-1" style="display: block;" aria-modal="true" role="dialog">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Doctor Notes</h5>
            <button type="button" class="btn-close" aria-label="Close" @click="$emit('close')"></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="doctor-name" class="form-label">Doctor Name</label>
                <input
                  id="doctor-name"
                  type="text"
                  class="form-control"
                  v-model="doctorName"
                  placeholder="Enter doctor name"
                />
              </div>
              <div class="mb-3">
                <label for="doctor-notes" class="form-label">Notes</label>
                <textarea
                  id="doctor-notes"
                  class="form-control"
                  v-model="notes"
                  placeholder="Enter notes"
                ></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="submitNotes">Submit</button>
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
        notes: '',
        doctorName: '',
      };
    },
    methods: {
      async submitNotes() {
        try {
          if (!this.appointment.id) {
            console.error('Missing appointment ID');
            return;
          }
          await axios.patch(`/api/appointments/${this.appointment.id}/doctor-notes/`, {
            doctor_notes: this.notes,
            doctor_name: this.doctorName,
          });
          Swal.fire({
            icon: 'success',
            title: 'Notes Added',
            text: 'Doctor notes have been successfully added!',
            showConfirmButton: false,
            timer: 2000,
          });
          this.$emit('close');
          this.$emit('refresh');
        } catch (error) {
          console.error('Error submitting notes:', error);
          Swal.fire({
            icon: 'error',
            title: 'Failed to Add Notes',
            text: 'An error occurred while adding notes. Please try again.',
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
  