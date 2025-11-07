<template>
  <div v-if="pageData">
    <HeroSection
      title="Where <span>Dogs</span> <br><img src='/assets/img/hero/client-img.png' alt='img'> Meets Strategy"
      description="We specialize in delivering cutting-edge solutions tailored to your needs. Whether you're looking you succeed."
      hero-image="/assets/img/hero/02.jpg"
      cta-text="Get Start a Project"
      cta-link="/contact"
      :stats="pageData.heroStats"
    />

    <BrandSliderSection
      heading="CLIENTS I'VE WORKED WITH"
      :brands="pageData.brands"
    />

    <ServiceSection
      subtitle="What We Can Do For You"
      title="Our Palette of <span>Expertise</span>"
      :services="pageData.services"
      variant="2"
      bg-section
    />

    <AboutSection
      subtitle="About Us"
      title="Crafting Creative <span>Solutions for</span> <br> Modern Brands"
      description="At the intersection of vision and execution, we bring creative compelling narratives,"
      variant="video"
      video-image="/assets/img/about/about-video.jpg"
      video-url="https://www.youtube.com/watch?v=Cn4G2lZ_g2I"
      :content-boxes="pageData.aboutBoxes"
      cta-text="More About Us"
      cta-link="/about"
    />

    <PortfolioSection
      subtitle="Our Portfolio"
      title="Some recent <span>work</span>"
      :projects="pageData.projects"
      variant="slider"
    />

    <TestimonialSection
      subtitle="Testimonial"
      title="Client <span>Feedback</span>"
      description="From concept to execution, Agenko nailed every aspect of our campaign. Their expertise and creativity have taken our brand to the next level."
      side-image="/assets/img/testimonial/testimonial.jpg"
      :testimonials="pageData.testimonials"
    />

    <TeamSection
      subtitle="Our Members"
      title="Meet The <span>Team</span>"
      :team="pageData.team"
      bg-section
      card-variant="card"
      :columns="3"
    />

    <BlogSection
      subtitle="Blog & News"
      title="Latest News & <span>Blog</span>"
      :posts="pageData.blogPosts"
    />
  </div>
</template>

<script setup lang="ts">
// All data is now fetched and processed within useAsyncData
// This stops the data from being included in the initial page bundle.
const { data: pageData } = await useAsyncData('index-data', async () => {
  // Asynchronously import data files
  const { services } = await import('~/data/services')
  const { team } = await import('~/data/team')
  const { projects } = await import('~/data/projects')
  const { stats, brands, testimonials, blogPosts } = await import('~/data/common')

  // Re-create heroStats from the original script
  const heroStats = [
    { ...stats[0] },
    { ...stats[1], active: true },
    { ...stats[2] }
  ]

  // Re-create aboutBoxes from the original script
  const aboutBoxes = [
    {
      title: 'Our Mission',
      description: 'Our mission is to empower brands by crafting innovative and impactful creative solutions. needs strategic campaigns success.'
    },
    {
      title: 'Our Vision',
      description: 'Our vision is to be the leading creative agency that redefines how brands connect with the push the boundaries of creativity,'
    }
  ]

  // Return one single object containing all page data
  return {
    heroStats,
    brands,
    services: services.slice(0, 3), // Pre-slice services here
    aboutBoxes,
    projects,
    testimonials,
    team,
    blogPosts
  }
})

// SEO metadata
useHead({
  title: 'Agznko - Creative Agency and Portfolio',
  meta: [
    { name: 'description', content: 'Where Creativity Meets Strategy - A creative agency specializing in design and digital solutions' }
  ]
})
</script>

<style scoped>

.body-bg {
  background-image: url('/assets/img/space-background.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  background-repeat: no-repeat;
  position: relative;
}

.body-bg::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(20, 20, 20, 0.85); /* Dark overlay - adjust opacity */
  z-index: -1;
}

</style>