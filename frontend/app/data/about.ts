/**
 * About Page Data
 * Information about the organization
 */

export interface AboutStats {
  number: string
  label: string
  suffix?: string
}

export interface AboutContent {
  title: string
  subtitle: string
  description: string
  videoUrl?: string
  videoImage?: string
  stats: AboutStats[]
  features: {
    icon: string
    title: string
    description: string
  }[]
  mission: string
  vision: string
  values: {
    title: string
    description: string
  }[]
}

export const aboutContent: AboutContent = {
  title: 'About Our Organization',
  subtitle: 'Charting the Stars Together',
  description: 'We are a diverse community of pilots, explorers, traders, and combat specialists united by our passion for adventure in the verse. Founded in 2947, our organization has grown into one of the most respected and capable groups in Star Citizen.',
  videoUrl: 'https://www.youtube.com/watch?v=example',
  videoImage: '/assets/img/about/video-thumb.jpg',

  stats: [
    {
      number: '500',
      label: 'Active Members',
      suffix: '+'
    },
    {
      number: '100',
      label: 'Systems Explored',
      suffix: '+'
    },
    {
      number: '6',
      label: 'Specialized Divisions'
    },
    {
      number: '1000',
      label: 'Missions Completed',
      suffix: '+'
    }
  ],

  features: [
    {
      icon: '/assets/img/icon/feature-01.svg',
      title: 'Professional Leadership',
      description: 'Experienced commanders guide our operations with strategic vision and tactical expertise, ensuring mission success.'
    },
    {
      icon: '/assets/img/icon/feature-02.svg',
      title: 'Active Community',
      description: 'Join a thriving community of dedicated players who share your passion for exploration, combat, and adventure.'
    },
    {
      icon: '/assets/img/icon/feature-03.svg',
      title: 'Diverse Operations',
      description: 'From combat missions to exploration and trading, we offer opportunities for every type of pilot to excel.'
    },
    {
      icon: '/assets/img/icon/feature-04.svg',
      title: 'Top-Tier Equipment',
      description: 'Access to organizational ships and equipment ensures you have the tools needed for any mission.'
    }
  ],

  mission: 'To build a premier Star Citizen organization that excels across all gameplay pillars while fostering a welcoming, professional community where every member can thrive and contribute to our collective success.',

  vision: 'To become the most respected and capable organization in the verse, known for our operational excellence, community spirit, and commitment to helping every member achieve their goals in Star Citizen.',

  values: [
    {
      title: 'Teamwork',
      description: 'We succeed together. Every mission, every operation depends on our ability to work as a coordinated team.'
    },
    {
      title: 'Excellence',
      description: 'We strive for excellence in everything we do, from combat operations to exploration missions and community events.'
    },
    {
      title: 'Respect',
      description: 'We treat all members with respect, regardless of experience level or preferred gameplay style.'
    },
    {
      title: 'Fun',
      description: 'Above all, we remember that Star Citizen is a game. We prioritize enjoyment and camaraderie in all activities.'
    }
  ]
}

export const aboutHistory = {
  title: 'Our History',
  timeline: [
    {
      year: '2947',
      title: 'Foundation',
      description: 'Organization founded by a small group of veteran pilots with a vision for collaborative gameplay.'
    },
    {
      year: '2948',
      title: 'Expansion',
      description: 'Added Exploration and Trading divisions. Reached 100 members milestone.'
    },
    {
      year: '2949',
      title: 'Diversification',
      description: 'Launched Mining and Intelligence divisions. Expanded operational capabilities across all gameplay pillars.'
    },
    {
      year: '2950',
      title: 'Medical Corps',
      description: 'Established Medical Division to support all operations with rescue and healthcare services.'
    },
    {
      year: '2951-2953',
      title: 'Growth & Excellence',
      description: 'Continued growth and refinement of all divisions. Became recognized as a premier organization in the verse.'
    }
  ]
}
