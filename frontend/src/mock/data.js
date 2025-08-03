// Mock data for Bazari platform
export const mockCategories = [
  {
    id: '1',
    name: 'الإلكترونيات',
    nameEn: 'Electronics',
    icon: 'smartphone',
    subCategories: ['هواتف ذكية', 'حاسوب وتابلت', 'اكسسوارات إلكترونية']
  },
  {
    id: '2',
    name: 'الأزياء',
    nameEn: 'Fashion',
    icon: 'shirt',
    subCategories: ['ملابس رجالية', 'ملابس نسائية', 'أحذية', 'حقائب واكسسوارات']
  },
  {
    id: '3',
    name: 'المنزل والحديقة',
    nameEn: 'Home & Garden',
    icon: 'home',
    subCategories: ['أثاث', 'ديكور المنزل', 'أدوات المطبخ', 'نباتات وحدائق']
  },
  {
    id: '4',
    name: 'الجمال والعناية',
    nameEn: 'Beauty & Care',
    icon: 'sparkles',
    subCategories: ['مستحضرات التجميل', 'العناية بالبشرة', 'العطور', 'العناية بالشعر']
  },
  {
    id: '5',
    name: 'الرياضة واللياقة',
    nameEn: 'Sports & Fitness',
    icon: 'dumbbell',
    subCategories: ['معدات رياضية', 'ملابس رياضية', 'مكملات غذائية']
  },
  {
    id: '6',
    name: 'الكتب والتعليم',
    nameEn: 'Books & Education',
    icon: 'book',
    subCategories: ['كتب', 'أدوات مكتبية', 'ألعاب تعليمية']
  }
];

export const mockProducts = [
  {
    id: '1',
    title: 'هاتف سامسونج جالاكسي S24',
    titleEn: 'Samsung Galaxy S24',
    price: 3299,
    originalPrice: 3599,
    currency: 'ر.س',
    rating: 4.8,
    reviewCount: 234,
    image: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80',
    images: [
      'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80'
    ],
    category: 'الإلكترونيات',
    seller: {
      id: '1',
      name: 'متجر التقنية المتقدمة',
      rating: 4.9,
      location: 'الرياض، السعودية'
    },
    description: 'هاتف سامسونج جالاكسي S24 الجديد مع أحدث التقنيات وكاميرا عالية الجودة. يأتي مع ضمان لمدة عامين ومواصفات ممتازة للاستخدام اليومي.',
    specifications: [
      { key: 'الشاشة', value: '6.2 بوصة Dynamic AMOLED' },
      { key: 'المعالج', value: 'Snapdragon 8 Gen 3' },
      { key: 'الذاكرة', value: '8GB RAM, 256GB' },
      { key: 'الكاميرا', value: '50MP + 12MP + 10MP' },
      { key: 'البطارية', value: '4000mAh' }
    ],
    inStock: true,
    stockQuantity: 15,
    discount: 8,
    isNew: true,
    isFeatured: true
  },
  {
    id: '2',
    title: 'فستان أنيق للسهرات',
    titleEn: 'Elegant Evening Dress',
    price: 450,
    originalPrice: 520,
    currency: 'ر.س',
    rating: 4.6,
    reviewCount: 89,
    image: 'https://images.unsplash.com/photo-1566479179817-1b8d14f5ca6b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80',
    images: [
      'https://images.unsplash.com/photo-1566479179817-1b8d14f5ca6b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1544441893-675973e31985?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80'
    ],
    category: 'الأزياء',
    seller: {
      id: '2',
      name: 'بوتيك الأناقة',
      rating: 4.7,
      location: 'دبي، الإمارات'
    },
    description: 'فستان أنيق مثالي للسهرات والمناسبات الخاصة. مصنوع من أجود الأقمشة ومتوفر بألوان مختلفة.',
    specifications: [
      { key: 'المقاس', value: 'S, M, L, XL' },
      { key: 'اللون', value: 'أزرق، أسود، أحمر' },
      { key: 'القماش', value: 'حرير طبيعي' },
      { key: 'العناية', value: 'غسيل جاف فقط' }
    ],
    inStock: true,
    stockQuantity: 8,
    discount: 13,
    isNew: false,
    isFeatured: true
  },
  {
    id: '3',
    title: 'طقم أواني مطبخ مميز',
    titleEn: 'Premium Kitchen Cookware Set',
    price: 680,
    originalPrice: 780,
    currency: 'ر.س',
    rating: 4.9,
    reviewCount: 156,
    image: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80',
    images: [
      'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80'
    ],
    category: 'المنزل والحديقة',
    seller: {
      id: '3',
      name: 'متجر المنزل الذكي',
      rating: 4.8,
      location: 'القاهرة، مصر'
    },
    description: 'طقم أواني مطبخ فاخر يتضمن جميع القطع الأساسية للطبخ. مصنوع من مواد عالية الجودة ومقاوم للخدش.',
    specifications: [
      { key: 'المادة', value: 'ستانلس ستيل + طلاء سيراميك' },
      { key: 'عدد القطع', value: '12 قطعة' },
      { key: 'الاستخدام', value: 'جميع أنواع المواقد' },
      { key: 'الضمان', value: '5 سنوات' }
    ],
    inStock: true,
    stockQuantity: 25,
    discount: 13,
    isNew: true,
    isFeatured: false
  },
  {
    id: '4',
    title: 'ساعة ذكية رياضية',
    titleEn: 'Smart Sports Watch',
    price: 899,
    originalPrice: 999,
    currency: 'ر.س',
    rating: 4.5,
    reviewCount: 312,
    image: 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80',
    images: [
      'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80'
    ],
    category: 'الإلكترونيات',
    seller: {
      id: '4',
      name: 'عالم الساعات الذكية',
      rating: 4.6,
      location: 'الكويت، الكويت'
    },
    description: 'ساعة ذكية متطورة لمتابعة الأنشطة الرياضية والصحة. تشمل ميزات متقدمة ومقاومة للماء.',
    specifications: [
      { key: 'الشاشة', value: '1.4 بوصة OLED' },
      { key: 'البطارية', value: 'تدوم حتى 7 أيام' },
      { key: 'المقاومة', value: 'IP68 مقاومة للماء' },
      { key: 'الاتصال', value: 'Bluetooth 5.0' }
    ],
    inStock: true,
    stockQuantity: 42,
    discount: 10,
    isNew: false,
    isFeatured: true
  },
  {
    id: '5',
    title: 'عطر فاخر للرجال',
    titleEn: 'Luxury Men\'s Perfume',
    price: 320,
    originalPrice: 380,
    currency: 'ر.س',
    rating: 4.7,
    reviewCount: 78,
    image: 'https://images.unsplash.com/photo-1541643600914-78c9e8f9e01b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80',
    images: [
      'https://images.unsplash.com/photo-1541643600914-78c9e8f9e01b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80'
    ],
    category: 'الجمال والعناية',
    seller: {
      id: '5',
      name: 'عالم العطور الشرقية',
      rating: 4.9,
      location: 'جدة، السعودية'
    },
    description: 'عطر فاخر بتركيبة شرقية أصيلة. يدوم طويلاً ومناسب لجميع المناسبات.',
    specifications: [
      { key: 'الحجم', value: '100ml' },
      { key: 'التركيز', value: 'Eau de Parfum' },
      { key: 'الرائحة', value: 'عود، ورد، مسك' },
      { key: 'الثبات', value: '8-12 ساعة' }
    ],
    inStock: true,
    stockQuantity: 18,
    discount: 16,
    isNew: false,
    isFeatured: false
  },
  {
    id: '6',
    title: 'حقيبة يد نسائية أنيقة',
    titleEn: 'Elegant Women\'s Handbag',
    price: 280,
    originalPrice: 320,
    currency: 'ر.س',
    rating: 4.4,
    reviewCount: 95,
    image: 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80',
    images: [
      'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80'
    ],
    category: 'الأزياء',
    seller: {
      id: '2',
      name: 'بوتيك الأناقة',
      rating: 4.7,
      location: 'دبي، الإمارات'
    },
    description: 'حقيبة يد أنيقة مصنوعة من الجلد الطبيعي. تصميم عصري ومساحة واسعة.',
    specifications: [
      { key: 'المادة', value: 'جلد طبيعي' },
      { key: 'الأبعاد', value: '30 × 25 × 15 سم' },
      { key: 'اللون', value: 'أسود، بني، أزرق' },
      { key: 'الإغلاق', value: 'سحاب ومغناطيس' }
    ],
    inStock: true,
    stockQuantity: 12,
    discount: 13,
    isNew: false,
    isFeatured: false
  }
];

export const mockSellers = [
  {
    id: '1',
    name: 'متجر التقنية المتقدمة',
    nameEn: 'Advanced Tech Store',
    rating: 4.9,
    reviewCount: 1243,
    location: 'الرياض، السعودية',
    joinDate: '2021-03-15',
    logo: 'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=100&q=80',
    banner: 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    description: 'متخصصون في بيع أحدث الأجهزة الإلكترونية والتقنية بأفضل الأسعار وضمان شامل.',
    categories: ['الإلكترونيات', 'اكسسوارات إلكترونية'],
    productCount: 156,
    isVerified: true,
    policies: {
      shipping: 'شحن مجاني للطلبات أكثر من 500 ريال',
      returns: 'إرجاع مجاني خلال 30 يوم',
      warranty: 'ضمان شامل لجميع المنتجات'
    }
  },
  {
    id: '2',
    name: 'بوتيك الأناقة',
    nameEn: 'Elegance Boutique',
    rating: 4.7,
    reviewCount: 867,
    location: 'دبي، الإمارات',
    joinDate: '2020-08-22',
    logo: 'https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=100&q=80',
    banner: 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    description: 'أزياء نسائية راقية وحقائب وإكسسوارات من أفضل الماركات العالمية.',
    categories: ['الأزياء', 'حقائب واكسسوارات'],
    productCount: 89,
    isVerified: true,
    policies: {
      shipping: 'شحن سريع خلال 24 ساعة',
      returns: 'إرجاع مجاني خلال 15 يوم',
      warranty: 'ضمان الجودة'
    }
  }
];

export const mockReviews = [
  {
    id: '1',
    productId: '1',
    userId: '101',
    userName: 'أحمد محمد',
    rating: 5,
    comment: 'منتج ممتاز جداً، الجودة عالية والتسليم سريع. أنصح بالشراء.',
    date: '2024-01-15',
    helpful: 12,
    verified: true
  },
  {
    id: '2',
    productId: '1',
    userId: '102',
    userName: 'فاطمة علي',
    rating: 4,
    comment: 'هاتف رائع ولكن السعر مرتفع قليلاً. الأداء ممتاز.',
    date: '2024-01-10',
    helpful: 8,
    verified: true
  },
  {
    id: '3',
    productId: '2',
    userId: '103',
    userName: 'نور الدين',
    rating: 5,
    comment: 'فستان جميل جداً وجودة القماش ممتازة. وصل بسرعة وكان كما هو موضح.',
    date: '2024-01-12',
    helpful: 15,
    verified: true
  }
];

export const mockBanners = [
  {
    id: '1',
    title: 'تخفيضات الجمعة البيضاء',
    subtitle: 'خصومات تصل إلى 70% على جميع المنتجات',
    image: 'https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    cta: 'تسوق الآن',
    link: '/categories'
  },
  {
    id: '2',
    title: 'إلكترونيات جديدة',
    subtitle: 'اكتشف أحدث الأجهزة والتقنيات',
    image: 'https://images.unsplash.com/photo-1498049794561-7780e7231661?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
    cta: 'استكشف',
    link: '/categories/electronics'
  }
];