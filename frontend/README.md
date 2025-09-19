# GRC Platform Frontend

Modern React-based frontend for the GRC (Governance, Risk, and Compliance) Platform, built with Material-UI and following feature-based architecture patterns.

## Architecture

The frontend follows a feature-based architecture with modern React patterns:

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── common/         # Common/shared components
│   │   └── layout/         # Layout components
│   ├── features/           # Feature-based modules
│   │   ├── dashboard/      # Dashboard feature
│   │   ├── compliance/     # Compliance management
│   │   ├── risk/          # Risk management
│   │   ├── policy/        # Policy management
│   │   ├── workflow/      # Workflow management
│   │   ├── ai-agents/     # AI agents management
│   │   ├── analytics/     # Analytics and reporting
│   │   └── settings/      # Settings and configuration
│   ├── services/          # API and external services
│   │   ├── api/           # API client and endpoints
│   │   ├── auth/          # Authentication services
│   │   └── websocket/     # WebSocket connections
│   ├── store/             # State management (Redux Toolkit)
│   │   ├── slices/        # Redux slices
│   │   └── middleware/    # Custom middleware
│   ├── hooks/             # Custom React hooks
│   │   ├── custom/        # Custom business hooks
│   │   └── api/           # API-related hooks
│   ├── utils/             # Utility functions
│   │   ├── helpers/       # Helper functions
│   │   ├── constants/     # Application constants
│   │   └── validators/    # Validation utilities
│   ├── types/             # TypeScript type definitions
│   │   ├── api/           # API types
│   │   └── components/    # Component types
│   └── assets/            # Static assets
│       ├── images/        # Image assets
│       ├── icons/         # Icon assets
│       └── styles/        # Global styles
├── public/                # Public assets
└── tests/                 # Test suites
    ├── unit/             # Unit tests
    ├── integration/      # Integration tests
    └── e2e/             # End-to-end tests
```

## Features

### Core Features
- **Dashboard** - Overview of GRC metrics and KPIs
- **Compliance Management** - Compliance assessments and evidence tracking
- **Risk Management** - Risk identification, assessment, and treatment
- **Policy Management** - Policy creation, review, and approval workflows
- **Workflow Management** - Business process automation and task management
- **AI Agents** - AI-powered analysis and recommendations
- **Analytics** - Advanced reporting and data visualization
- **Settings** - User and system configuration

### Technical Features
- **Responsive Design** - Mobile-first, responsive UI
- **Real-time Updates** - WebSocket integration for live data
- **Advanced Data Tables** - Sortable, filterable, paginated tables
- **Interactive Charts** - Dynamic charts and visualizations
- **Search & Filter** - Advanced search and filtering capabilities
- **Export Functionality** - PDF and Excel export options
- **Dark/Light Theme** - Theme switching support
- **Accessibility** - WCAG 2.1 AA compliance

## Getting Started

### Prerequisites
- Node.js 18+
- npm 9+ or yarn 1.22+
- Backend services running (see backend README)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd grc-platform/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

4. **Start development server**
   ```bash
   npm start
   # or
   yarn start
   ```

The application will be available at http://localhost:3000

### Building for Production

```bash
# Build the application
npm run build
# or
yarn build

# Serve the built application
npm run serve
# or
yarn serve
```

## Development

### Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint issues
- `npm run type-check` - Run TypeScript type checking

### Code Style

- **ESLint** for code linting
- **Prettier** for code formatting
- **TypeScript** for type safety
- **Husky** for git hooks

```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Type check
npm run type-check
```

### Adding New Features

1. **Create feature directory** in `src/features/`
2. **Add components** specific to the feature
3. **Create API services** in `src/services/api/`
4. **Add Redux slices** in `src/store/slices/`
5. **Create custom hooks** in `src/hooks/`
6. **Add types** in `src/types/`
7. **Write tests** in `tests/`

### Component Structure

Each feature should follow this structure:

```
features/feature-name/
├── components/           # Feature-specific components
├── hooks/               # Feature-specific hooks
├── services/            # Feature-specific services
├── types/               # Feature-specific types
├── utils/               # Feature-specific utilities
└── index.ts             # Feature exports
```

## Configuration

Environment variables are managed through `.env.local`:

```env
# API Configuration
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_API_TIMEOUT=30000

# WebSocket Configuration
REACT_APP_WS_URL=ws://localhost:8000/ws

# Feature Flags
REACT_APP_ENABLE_AI_AGENTS=true
REACT_APP_ENABLE_ANALYTICS=true
REACT_APP_ENABLE_DARK_MODE=true

# External Services
REACT_APP_GOOGLE_ANALYTICS_ID=your_ga_id
REACT_APP_SENTRY_DSN=your_sentry_dsn
```

## Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage

# Run specific test types
npm run test:unit          # Unit tests
npm run test:integration   # Integration tests
npm run test:e2e          # End-to-end tests
```

### Testing Strategy

- **Unit Tests** - Component and utility function testing
- **Integration Tests** - API integration and user flows
- **E2E Tests** - Complete user journey testing
- **Visual Regression Tests** - UI consistency testing

## State Management

The application uses Redux Toolkit for state management:

- **Slices** - Feature-based state slices
- **Middleware** - Custom middleware for API calls and logging
- **Selectors** - Memoized selectors for efficient data access
- **Async Thunks** - Async action creators for API calls

## API Integration

- **Axios** for HTTP requests
- **React Query** for data fetching and caching
- **WebSocket** for real-time updates
- **Error Handling** - Centralized error handling and user feedback

## Styling

- **Material-UI** - Component library and theming
- **Emotion** - CSS-in-JS styling
- **Responsive Design** - Mobile-first approach
- **Theme System** - Light/dark theme support

## Performance

- **Code Splitting** - Route-based code splitting
- **Lazy Loading** - Component lazy loading
- **Memoization** - React.memo and useMemo optimization
- **Bundle Analysis** - Webpack bundle analyzer integration

## Accessibility

- **ARIA Labels** - Proper ARIA labeling
- **Keyboard Navigation** - Full keyboard support
- **Screen Reader** - Screen reader compatibility
- **Color Contrast** - WCAG AA color contrast compliance

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Ensure all checks pass
6. Submit a pull request

## License

MIT License - see LICENSE file for details.
