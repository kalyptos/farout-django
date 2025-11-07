<template>
  <div>
    <!-- Page Header -->
    <PageHeader
      title="Contact Us"
      subtitle="Get In Touch"
      :breadcrumbs="[
        { label: 'Home', path: '/' },
        { label: 'Contact', path: '/contact' }
      ]"
    />

    <!-- Contact Info Boxes -->
    <ContactInfo />

    <!-- Contact Form & Map -->
    <ContactForm />
  </div>
</template>

<script setup lang="ts">
useHead({
  title: 'Contact Us - Far Out',
  meta: [
    {
      name: 'description',
      content: 'Get in touch with Far Out. Contact us for more information about our Star Citizen organization.'
    }
  ]
})
</script>
