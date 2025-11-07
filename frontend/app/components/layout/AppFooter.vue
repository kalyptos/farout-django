<template>
  <footer class="footer-section fix" :class="[variant === 'style-2' ? 'section-bg style-2' : '']">
    <div class="container">
      <div class="row" v-if="variant === 'style-2'">
        <!-- Style 2: Split layout with CTA on right -->
        <div class="col-xxl-10">
          <div class="container">
            <div class="footer-widgets-wrapper">
              <div class="row">
                <!-- Logo & Description -->
                                <AnimatedElement animation="fade-in-up" :delay="'.2s'" class="col-xl-5 col-lg-4 col-md-6">
                  <div class="single-footer-widget">
                    <div class="widget-head">
                      <NuxtLink to="/">
                        <NuxtImg src="/assets/img/logo/white-logo.svg" alt="logo" />
                      </NuxtLink>
                    </div>
                    <div class="footer-content">
                      <p>
                        Agenko All Rights Reserved. Designed <br> with passion, Let's create something <br> amazing together.
                      </p>
                      <div class="social-icon d-flex align-items-center">
                        <a href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                        <a href="#" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
                        <a href="#" aria-label="Vimeo"><i class="fab fa-vimeo-v"></i></a>
                        <a href="#" aria-label="Pinterest"><i class="fab fa-pinterest-p"></i></a>
                      </div>
                    </div>
                  </div>
                </AnimatedElement>

                <!-- Explore Links -->
                                <AnimatedElement animation="fade-in-up" :delay="'.4s'" class="col-xl-3 col-lg-4 col-md-6 ps-lg-3">
                  <div class="single-footer-widget">
                    <div class="widget-head">
                      <h3>Explore</h3>
                    </div>
                    <ul class="list-items">
                      <li><NuxtLink to="/about">About Us</NuxtLink></li>
                      <li><NuxtLink to="/divisions">Divisions</NuxtLink></li>
                      <li><NuxtLink to="/members">Members</NuxtLink></li>
                      <li><NuxtLink to="/blog">Our Blog</NuxtLink></li>
                      <li><NuxtLink to="/contact">Contact Us</NuxtLink></li>
                    </ul>
                  </div>
                </AnimatedElement>

                <!-- Contact Info -->
                                <AnimatedElement animation="fade-in-up" :delay="'.6s'" class="col-xl-4 col-lg-4 col-md-6 ps-lg-5">
                  <div class="single-footer-widget">
                    <div class="widget-head">
                      <h3>Contact Us</h3>
                    </div>
                    <div class="footer-content">
                      <p>4517 Washington. Manchester, Kentucky 39495</p>
                      <div class="contact-text">
                        <h4 class="pb-3"><a href="tel:6035550123">(603) 555-0123</a></h4>
                        <h5><a href="mailto:info@example.com">info@example.com</a></h5>
                      </div>
                    </div>
                  </div>
                </AnimatedElement>
              </div>
            </div>

            <!-- Footer Bottom -->
            <div class="footer-bottom">
              <div class="footer-bottom-wrapper">
                                <AnimatedElement animation="fade-in-up" :delay="'.3s'">
                  <p>Copyright @ 2024 Agenko</p>
                </AnimatedElement>
                <AnimatedElement animation="fade-in-up" :delay="'.5s'">
                  <p>Designed By <a href="#">wordpressriver</a></p>
                </AnimatedElement>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side CTA -->
        <div class="col-xxl-2">
          <div class="footer-right-content">
                        <AnimatedElement animation="fade-in-up" :delay="'.3s'">
              <h2>
                Have a Project in <br> Your Mind?
              </h2>
            </AnimatedElement>
                        <AnimatedElement animation="fade-in-up" :delay="'.5s'">
              <NuxtLink to="/contact" class="radius-btn">
                <i class="fa-sharp fa-solid fa-arrow-right"></i>
                Contact Us
              </NuxtLink>
            </AnimatedElement>
                        <AnimatedElement animation="fade-in-up" :delay="'.6s'">
              <h4>07 : 00 AM - 12 : 30 PM</h4>
            </AnimatedElement>
            <AnimatedElement animation="fade-in-up" :delay="'.7s'">
              <p>Saturday - Thursday</p>
            </AnimatedElement>
          </div>
        </div>
      </div>

      <!-- Standard Footer Layout (Variant 1) -->
      <div v-else>
        <div class="footer-widgets-wrapper">
          <div class="row">
            <!-- Logo & Description -->
                        <AnimatedElement animation="fade-in-up" :delay="'.2s'" class="col-xl-4 col-lg-4 col-md-6">
              <div class="single-footer-widget">
                <div class="widget-head">
                  <NuxtLink to="/">
                    <NuxtImg src="/assets/img/logo/white-logo.svg" alt="logo" />
                  </NuxtLink>
                </div>
                <div class="footer-content">
                  <p>
                    Agenko All Rights Reserved. Designed <br> with passion, Let's create something <br> amazing together.
                  </p>
                  <div class="social-icon d-flex align-items-center">
                    <a href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                    <a href="#" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
                    <a href="#" aria-label="Vimeo"><i class="fab fa-vimeo-v"></i></a>
                    <a href="#" aria-label="Pinterest"><i class="fab fa-pinterest-p"></i></a>
                  </div>
                </div>
              </div>
            </AnimatedElement>

            <!-- Quick Links -->
                        <AnimatedElement animation="fade-in-up" :delay="'.4s'" class="col-xl-2 col-lg-4 col-md-6 ps-lg-3">
              <div class="single-footer-widget">
                <div class="widget-head">
                  <h3>Quick Links</h3>
                </div>
                <ul class="list-items">
                  <li><NuxtLink to="/about">About Us</NuxtLink></li>
                  <li><NuxtLink to="/divisions">Divisions</NuxtLink></li>
                  <li><NuxtLink to="/members">Members</NuxtLink></li>
                  <li><NuxtLink to="/blog">Our Blog</NuxtLink></li>
                  <li><NuxtLink to="/contact">Contact Us</NuxtLink></li>
                </ul>
              </div>
            </AnimatedElement>

            <!-- Office Info -->
                        <AnimatedElement animation="fade-in-up" :delay="'.6s'" class="col-xl-3 col-lg-4 col-md-6 ps-lg-5">
              <div class="single-footer-widget">
                <div class="widget-head">
                  <h3>Office</h3>
                </div>
                <div class="footer-content">
                  <p>4517 Washington. Manchester, Kentucky 39495</p>
                  <div class="contact-text">
                    <h4 class="pb-3"><a href="tel:6035550123">(603) 555-0123</a></h4>
                    <h5><a href="mailto:info@example.com">info@example.com</a></h5>
                  </div>
                </div>
              </div>
            </AnimatedElement>

            <!-- Newsletter -->
                        <AnimatedElement animation="fade-in-up" :delay="'.8s'" class="col-xl-3 col-lg-4 col-md-6 ps-lg-3">
              <div class="single-footer-widget">
                <div class="widget-head">
                  <h3>Subscribe to our newsletter</h3>
                </div>
                <div class="footer-content">
                  <div class="footer-input">
                    <input
                      v-model="email"
                      type="email"
                      id="email"
                      placeholder="Enter your email"
                    />
                    <button class="newsletter-btn" type="submit" @click="handleNewsletter" aria-label="Subscribe">
                      <i class="fa-sharp fa-light fa-paper-plane"></i>
                    </button>
                  </div>
                </div>
              </div>
            </AnimatedElement>
          </div>
        </div>

        <!-- Footer Bottom -->
        <div class="footer-bottom">
          <div class="footer-bottom-wrapper">
                        <AnimatedElement animation="fade-in-up" :delay="'.3s'">
              <p>Copyright @ 2024 Agenko</p>
            </AnimatedElement>
            <AnimatedElement animation="fade-in-up" :delay="'.5s'">
              <p>Designed By <a href="#">wordpressriver</a></p>
            </AnimatedElement>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  variant?: 'default' | 'style-2'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default'
})

const email = ref('')

const handleNewsletter = () => {
  if (email.value && email.value.includes('@')) {
    // TODO: Implement newsletter subscription logic
    // Could POST to /api/newsletter or use a third-party service
    // await $fetch('/api/newsletter', { method: 'POST', body: { email: email.value } })
    email.value = ''
  }
}
</script>

<style scoped>
/* Footer styles are handled by the main template CSS */
</style>
