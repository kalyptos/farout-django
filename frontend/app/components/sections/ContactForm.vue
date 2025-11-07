<template>
  <section class="contact-section fix section-padding pt-0">
    <div class="container">
      <div class="contact-wrapper">
        <div class="row">
          <!-- Map Section -->
          <div class="col-lg-6">
            <div class="map-items">
              <div class="googpemap">
                <iframe
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3022.1422937950147!2d-73.98731968459391!3d40.74844097932681!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c259a9b3117469%3A0xd134e199a405a163!2sEmpire%20State%20Building!5e0!3m2!1sen!2sus!4v1234567890123!5m2!1sen!2sus"
                  style="border:0; width: 100%; height: 100%; min-height: 400px;"
                  allowfullscreen=""
                  loading="lazy"
                ></iframe>
              </div>
            </div>
          </div>

          <!-- Contact Form -->
          <div class="col-lg-6">
            <div class="contact-content">
              <div class="section-title text-center">
                <h6 data-aos="fade-up">Contact Us</h6>
                <h2 data-aos="fade-up" data-aos-delay="300">Get in touch</h2>
              </div>

              <form
                @submit.prevent="handleSubmit"
                class="contact-form-items mt-3 mt-md-0"
              >
                <div class="row g-4">
                  <!-- Name Field -->
                  <div class="col-lg-6" data-aos="fade-up" data-aos-delay="300">
                    <div class="form-clt">
                      <span>Your name*</span>
                      <input
                        v-model="formData.name"
                        type="text"
                        name="name"
                        id="name"
                        placeholder="Your Name"
                        required
                      >
                      <span v-if="errors.name" class="error">{{ errors.name }}</span>
                    </div>
                  </div>

                  <!-- Email Field -->
                  <div class="col-lg-6" data-aos="fade-up" data-aos-delay="500">
                    <div class="form-clt">
                      <span>Your Email*</span>
                      <input
                        v-model="formData.email"
                        type="email"
                        name="email"
                        id="email"
                        placeholder="Your Email"
                        required
                      >
                      <span v-if="errors.email" class="error">{{ errors.email }}</span>
                    </div>
                  </div>

                  <!-- Message Field -->
                  <div class="col-lg-12" data-aos="fade-up" data-aos-delay="700">
                    <div class="form-clt">
                      <span>Write Message*</span>
                      <textarea
                        v-model="formData.message"
                        name="message"
                        id="message"
                        placeholder="Write Message"
                        rows="5"
                        required
                      ></textarea>
                      <span v-if="errors.message" class="error">{{ errors.message }}</span>
                    </div>
                  </div>

                  <!-- Submit Button -->
                  <div class="col-lg-7" data-aos="fade-up" data-aos-delay="900">
                    <button
                      type="submit"
                      class="theme-btn"
                      :disabled="isSubmitting"
                    >
                      {{ isSubmitting ? 'Sending...' : 'Send Message' }}
                    </button>
                  </div>

                  <!-- Success/Error Message -->
                  <div v-if="submitMessage" class="col-lg-12">
                    <div
                      class="alert"
                      :class="submitSuccess ? 'alert-success' : 'alert-danger'"
                    >
                      {{ submitMessage }}
                    </div>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import type { ContactFormData } from '~/data/contact'

const formData = reactive<ContactFormData>({
  name: '',
  email: '',
  message: ''
})

const errors = reactive({
  name: '',
  email: '',
  message: ''
})

const isSubmitting = ref(false)
const submitMessage = ref('')
const submitSuccess = ref(false)

// Validate email format
const validateEmail = (email: string): boolean => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

// Validate form
const validateForm = (): boolean => {
  let isValid = true

  // Reset errors
  errors.name = ''
  errors.email = ''
  errors.message = ''

  // Validate name
  if (!formData.name.trim()) {
    errors.name = 'Name is required'
    isValid = false
  }

  // Validate email
  if (!formData.email.trim()) {
    errors.email = 'Email is required'
    isValid = false
  } else if (!validateEmail(formData.email)) {
    errors.email = 'Please enter a valid email'
    isValid = false
  }

  // Validate message
  if (!formData.message.trim()) {
    errors.message = 'Message is required'
    isValid = false
  } else if (formData.message.trim().length < 10) {
    errors.message = 'Message must be at least 10 characters'
    isValid = false
  }

  return isValid
}

// Handle form submission
const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  isSubmitting.value = true
  submitMessage.value = ''

  try {
    // TODO: Replace with actual API endpoint
    // For now, simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Simulate success
    submitSuccess.value = true
    submitMessage.value = 'Thank you! Your message has been sent successfully.'

    // Reset form
    formData.name = ''
    formData.email = ''
    formData.message = ''

    // Clear success message after 5 seconds
    setTimeout(() => {
      submitMessage.value = ''
    }, 5000)
  } catch (error) {
    submitSuccess.value = false
    submitMessage.value = 'Sorry, there was an error sending your message. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style lang="scss" scoped>
.contact-section {
  padding: 60px 0 0;
}

.contact-wrapper {
  background-color: var(--background-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
}

.map-items {
  height: 100%;
  min-height: 500px;

  .googpemap {
    height: 100%;

    iframe {
      width: 100%;
      height: 100%;
    }
  }
}

.contact-content {
  padding: 40px;

  @media (max-width: 991px) {
    padding: 40px 20px;
  }

  .section-title {
    margin-bottom: 30px;

    h6 {
      font-size: 14px;
      text-transform: uppercase;
      color: var(--color-primary);
      margin-bottom: 10px;
      letter-spacing: 2px;
    }

    h2 {
      font-size: 36px;
      font-weight: 700;
      color: var(--text-heading);
      margin: 0;

      @media (max-width: 767px) {
        font-size: 28px;
      }
    }
  }
}

.contact-form-items {
  .form-clt {
    margin-bottom: 0;

    span {
      display: block;
      font-size: 14px;
      color: var(--text-secondary);
      margin-bottom: 8px;
      font-weight: 500;

      &.error {
        color: var(--error);
        font-size: 12px;
        margin-top: 5px;
      }
    }

    input,
    textarea {
      width: 100%;
      padding: 15px 20px;
      background-color: var(--background-light);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      color: var(--text-primary);
      font-size: 15px;
      transition: all 0.3s ease;

      &::placeholder {
        color: var(--text-muted);
      }

      &:focus {
        outline: none;
        border-color: var(--color-primary);
        background-color: var(--background-primary);
      }
    }

    textarea {
      resize: vertical;
      min-height: 120px;
    }
  }
}

.theme-btn {
  background-color: var(--button-primary-bg);
  color: var(--button-primary-text);
  padding: 16px 40px;
  border: none;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: capitalize;

  &:hover:not(:disabled) {
    background-color: var(--button-secondary-bg);
    color: var(--button-secondary-text);
    transform: translateY(-2px);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.alert {
  padding: 15px 20px;
  border-radius: 6px;
  font-size: 14px;
  margin-top: 20px;

  &.alert-success {
    background-color: rgba($success, 0.1);
    border: 1px solid var(--success);
    color: var(--success);
  }

  &.alert-danger {
    background-color: rgba($error, 0.1);
    border: 1px solid var(--error);
    color: var(--error);
  }
}
</style>
