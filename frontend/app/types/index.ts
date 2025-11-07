// Social Media Link
export interface SocialLink {
  platform: string
  url: string
  icon: string
}

// Service/Feature
export interface Service {
  id: string
  icon: string
  title: string
  description: string
  link: string
}

// Team Member
export interface TeamMember {
  id: string
  name: string
  role: string
  image: string
  bio?: string
  socialLinks: SocialLink[]
}

// Testimonial
export interface Testimonial {
  id: string
  content: string
  clientName: string
  clientRole: string
  clientImage: string
  rating: number
}

// Blog Post
export interface BlogPost {
  id: string
  title: string
  excerpt: string
  content?: string
  image: string
  date: string | Date
  author?: string
  category?: string
  slug: string
}

// Portfolio/Project
export interface Project {
  id: string
  title: string
  category: string
  description: string
  image: string
  hoverImage?: string
  slug: string
  client?: string
  date?: string
}

// Counter/Stat
export interface Stat {
  value: number
  unit?: string
  label: string
  prefix?: string
  suffix?: string
  active?: boolean
}

// Brand/Client Logo
export interface Brand {
  id: string
  name: string
  logo: string
  url?: string
}

// FAQ Item
export interface FaqItem {
  id: string
  question: string
  answer: string
}

// Pricing Plan
export interface PricingPlan {
  id: string
  name: string
  price: number
  currency?: string
  period?: string
  features: string[]
  featured?: boolean
  buttonText?: string
  buttonLink?: string
}

// Navigation Item
export interface NavItem {
  label: string
  link?: string
  children?: NavItem[]
}

// Contact Info
export interface ContactInfo {
  address: string
  email: string
  phone: string
  workingHours: string
}
