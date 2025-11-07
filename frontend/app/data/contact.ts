// ============================================================================
// CONTACT PAGE DATA
// ============================================================================

export interface ContactInfo {
  phone: string
  email: string
  address: string
  workingHours?: string
}

export interface ContactFormData {
  name: string
  email: string
  message: string
}

export const contactInfo: ContactInfo = {
  phone: '(704) 555-0127',
  email: 'info@example.com',
  address: 'Cedar Street, Chicago, 60601, USA',
  workingHours: 'Mon-Friday, 09am - 05pm'
}

export const contactBoxes = [
  {
    icon: 'fa-phone',
    title: 'Call Us For Support:',
    content: contactInfo.phone,
    link: `tel:${contactInfo.phone.replace(/\D/g, '')}`
  },
  {
    icon: 'fa-envelope',
    title: 'Email Us Anytime:',
    content: contactInfo.email,
    link: `mailto:${contactInfo.email}`
  },
  {
    icon: 'fa-map-marker-alt',
    title: 'Office Address',
    content: contactInfo.address,
    link: null
  }
]
