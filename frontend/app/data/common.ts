import type { Stat, Brand, Testimonial, BlogPost } from '~/types'

export const stats: Stat[] = [
  { value: 12, unit: '+', label: 'YEAR EXPERIENCE' },
  { value: 25, unit: 'k', label: 'HAPPY CUSTOMER' },
  { value: 8, unit: 'k', label: 'PROJECTS COMPLETED' },
  { value: 160, unit: '+', label: 'WINNING AWARD' }
]

export const brands: Brand[] = [
  { id: '1', name: 'Brand 1', logo: '/assets/img/brand/01.png' },
  { id: '2', name: 'Brand 2', logo: '/assets/img/brand/02.png' },
  { id: '3', name: 'Brand 3', logo: '/assets/img/brand/03.png' },
  { id: '4', name: 'Brand 4', logo: '/assets/img/brand/04.png' },
  { id: '5', name: 'Brand 5', logo: '/assets/img/brand/05.png' },
  { id: '6', name: 'Brand 6', logo: '/assets/img/brand/06.png' }
]

export const testimonials: Testimonial[] = [
  {
    id: '1',
    content: 'Agenko transformed our ideas into a stunning reality. Their innovative approach and dedication to our project were exceptional. We couldn\'t be happier with the results.',
    clientName: 'Brooklyn Simmons',
    clientRole: 'Nursing Assistant',
    clientImage: '/assets/img/testimonial/03.png',
    rating: 4.5
  },
  {
    id: '2',
    content: 'Agenko transformed our ideas into a stunning reality. Their innovative approach and dedication to our project were exceptional. We couldn\'t be happier with the results.',
    clientName: 'Theresa Webb',
    clientRole: 'Web Designer',
    clientImage: '/assets/img/testimonial/04.png',
    rating: 4.5
  },
  {
    id: '3',
    content: 'Agenko transformed our ideas into a stunning reality. Their innovative approach and dedication to our project were exceptional. We couldn\'t be happier with the results.',
    clientName: 'Kristin Watson',
    clientRole: 'President of Sales',
    clientImage: '/assets/img/testimonial/05.png',
    rating: 4.5
  },
  {
    id: '4',
    content: 'Agenko transformed our ideas into a stunning reality. Their innovative approach and dedication to our project were exceptional. We couldn\'t be happier with the results.',
    clientName: 'Malan David',
    clientRole: 'China',
    clientImage: '/assets/img/testimonial/06.png',
    rating: 4.5
  }
]

export const blogPosts: BlogPost[] = [
  {
    id: '1',
    title: 'The Art of Strategic Creativity',
    excerpt: 'Words matter, and our copy writing services ensure your message heard loud Whether and clear.',
    image: '/assets/img/news/04.jpg',
    date: 'August 17, 2024',
    slug: 'art-of-strategic-creativity'
  },
  {
    id: '2',
    title: 'Key Steps to Effective Rebranding',
    excerpt: 'Words matter, and our copy writing services ensure your message heard loud Whether and clear.',
    image: '/assets/img/news/05.jpg',
    date: 'August 17, 2024',
    slug: 'effective-rebranding'
  }
]
