# Frontend Guidelines

This document contains detailed frontend-specific guidelines for the GameAnnouncer project.

**Technology:** React 19.2, TypeScript 5.9, Vite 7.2+, MobX, Material-UI v7.3+, Axios, Formik, Yup

**IMPORTANT:** Ignore `frontend/` directory - it's a deprecated Angular app. Work only in `frontend-react/`.

---

## State Management (MobX)

**CRITICAL: Use MobX, NOT Redux**

### Basic Structure

```typescript
import { makeAutoObservable, runInAction } from 'mobx';
import { observer } from 'mobx-react-lite';

class GamesService {
  games: Game[] = [];
  isLoading = false;

  constructor() {
    makeAutoObservable(this);
  }

  async loadGames() {
    this.isLoading = true;
    try {
      const response = await gamesApi.getGames();
      runInAction(() => {
        this.games = response.data;
        this.isLoading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.isLoading = false;
      });
    }
  }
}
```

### Component Usage

Wrap components with `observer()` to react to observable changes:

```typescript
export const GamesPage = observer(() => {
  const { gamesService } = useRootService();

  useEffect(() => {
    gamesService.loadGames();
  }, []);

  return (
    <div>
      {gamesService.games.map(game => <GameCard key={game.id} game={game} />)}
    </div>
  );
});
```

### Critical Rules

1. **ALWAYS** use `runInAction()` when mutating state in async functions
2. **NEVER** mutate state directly outside `runInAction()`
3. **ALWAYS** wrap components that read observables with `observer()`

---

## Service Architecture

### Three-Layer Pattern

1. **API Services** (`/shared/services/api/`) - HTTP requests only
2. **Domain Services** - State management + business logic
3. **Root Service** - Container for all services

### API Service

Extend `BaseApiService` for HTTP operations:

```typescript
// shared/services/api/games-api.service.ts
export class GamesApiService extends BaseApiService {
  async getGames(params: IPaginationParams): Promise<PaginatedResponse<Game>> {
    return this.get('/api/v1/games', { params });
  }

  async getGameById(id: number): Promise<DataResponse<Game>> {
    return this.get(`/api/v1/games/${id}`);
  }

  async createGame(data: GameCreatePayload): Promise<DataResponse<Game>> {
    return this.post('/api/v1/games', data);
  }
}
```

### Domain Service

Manage state and orchestrate API calls:

```typescript
// services/games.service.ts
export class GamesService {
  pagination = new PaginationService<Game>();
  selectedGame: TMaybe<Game> = null;

  constructor(private api: GamesApiService) {
    makeAutoObservable(this);
  }

  async loadGames() {
    const response = await this.api.getGames({ skip: 0, limit: 20 });
    runInAction(() => {
      this.pagination.init(response);
    });
  }

  async deleteGame(id: number) {
    await this.api.deleteGame(id);
    runInAction(() => {
      this.pagination.removeItem(id);
    });
  }
}
```

### Root Service

Access all services via `useRootService()` hook:

```typescript
const { gamesService, authService } = useRootService();
```

---

## TypeScript

### Type Safety

**Strict mode is enabled - follow these rules:**

1. **ALWAYS** provide explicit types
2. **AVOID** `any` type - use `unknown` if type is truly unknown
3. **USE** type utilities: `TMaybe<T>`, `Partial<T>`, `Pick<T, K>`, `Omit<T, K>`

### Define Interfaces for API Types

```typescript
// GOOD
interface Game {
  id: number;
  name: string;
  description: string;
  image_url: TMaybe<string>;
  created_at: string;
}

type GameCreatePayload = Omit<Game, 'id' | 'created_at'>;

// BAD
const game: any = { ... };
```

---

## Components

### Component Structure

**Rules:**
- Functional components only (NO class components)
- Keep components small and focused
- Extract reusable components to `/shared/ui/`
- Use Material-UI components via `/shared/ui/` wrappers

**Example:**
```tsx
export const GameCard: FC<{ game: Game }> = observer(({ game }) => {
  const { gamesService } = useRootService();

  const handleDelete = async () => {
    await gamesService.deleteGame(game.id);
  };

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h6">{game.name}</Typography>
      <Typography variant="body2">{game.description}</Typography>
      <IconButton onClick={handleDelete}>
        <DeleteIcon />
      </IconButton>
    </Box>
  );
});
```

---

## Forms

### Formik + Yup

**Use Formik for form state and Yup for validation:**

```tsx
import { Formik, Form } from 'formik';
import * as Yup from 'yup';

const GameSchema = Yup.object({
  name: Yup.string().required('Name is required').max(255),
  description: Yup.string().required('Description is required'),
});

export const GameForm: FC = () => (
  <Formik
    initialValues={{ name: '', description: '' }}
    validationSchema={GameSchema}
    onSubmit={async (values) => {
      await gamesApi.createGame(values);
    }}
  >
    {({ errors, touched }) => (
      <Form>
        <TextField
          name="name"
          label="Name"
          error={touched.name && !!errors.name}
          helperText={touched.name && errors.name}
        />
        <TextField
          name="description"
          label="Description"
          error={touched.description && !!errors.description}
          helperText={touched.description && errors.description}
        />
      </Form>
    )}
  </Formik>
);
```

---

## HTTP Requests

### Axios via BaseApiService

**DO NOT create raw axios instances:**
- Use `BaseApiService` which provides:
  - Automatic JWT token injection
  - Auto token refresh on 401
  - Error notifications
  - Standardized error handling

**DO NOT add global error handling in components** - interceptors handle this.

---

## Styling

### Use `sx` prop

**Material-UI styling approach:**

```tsx
// GOOD - sx prop with theme values
<Box
  sx={{
    padding: 2,  // theme spacing
    backgroundColor: 'background.paper',  // theme color
    borderRadius: 1,  // theme shape
  }}
>
  ...
</Box>

// BAD - inline styles with hardcoded values
<Box style={{ padding: '16px', backgroundColor: '#fff' }}>
  ...
</Box>
```

### Styling Rules

1. **USE** `sx` prop for component styles
2. **USE** theme values (spacing, colors, breakpoints)
3. **USE** relative units (`rem`, `em`) NOT `px`
4. **AVOID** inline `style` prop
5. **AVOID** hardcoded values (colors, sizes)

---

## Routing

### React Router v7

**Routes location:** `/app/routes/`

**Use route constants:**

```typescript
// GOOD - use constants
import { appRoutes } from '@shared/constants/appRoutes';

<Route path={appRoutes.games} element={<GamesPage />} />

// BAD - hardcoded paths
<Route path="/games" element={<GamesPage />} />
```

---

## File Structure

### Layers

1. **Pages** (`/pages/`) - Route-level components
2. **Features** (`/features/`) - Feature-specific components
3. **Widgets** (`/widgets/`) - Reusable widget components
4. **Services** (`/shared/services/`) - State management and API
5. **UI** (`/shared/ui/`) - Design system components

### Naming Conventions

**Components:**
- `PascalCase.tsx` or `kebab-case.tsx` (be consistent)

**Services:**
- `kebab-case.ts` or `camelCase.ts`

**Hooks:**
- `use-hook-name.ts` or `useHookName.ts`

**Variables/Functions:**
- `camelCase` for functions and variables
- `PascalCase` for component names and types
- `UPPER_CASE` for constants

---

## Project Patterns

### Pagination

Use `PaginationService<T>` for infinite scroll:

```typescript
class GamesService {
  pagination = new PaginationService<Game>();

  async loadGames() {
    const response = await this.api.getGames({ skip: 0, limit: 20 });
    runInAction(() => {
      this.pagination.init(response);
    });
  }

  async loadMore() {
    const response = await this.api.getGames({
      skip: this.pagination.data.length,
      limit: 20,
    });
    runInAction(() => {
      this.pagination.append(response);
    });
  }
}
```

### Search/Filtering

Pass filter parameters to API:

```typescript
async searchGames(query: string) {
  const response = await this.api.getGames({
    skip: 0,
    limit: 20,
    search: query
  });
  runInAction(() => {
    this.pagination.init(response);
  });
}
```

---

## Performance

### Optimization Techniques

1. **React.memo()** - Memoize expensive components
2. **React.lazy()** - Code splitting for routes
3. **Debounce** - Debounce search inputs
4. **Infinite Scroll** - Use `PaginationService` instead of traditional pagination
5. **Image Optimization** - Use proper formats and lazy loading

**Example:**
```tsx
import { memo } from 'react';

export const GameCard = memo<{ game: Game }>(({ game }) => {
  return <div>{game.name}</div>;
});
```

---

## What NOT to Do

1. **DO NOT** use Redux (use MobX)
2. **DO NOT** use class components (use functional)
3. **DO NOT** mutate state outside `runInAction()`
4. **DO NOT** fetch data directly in components (use services)
5. **DO NOT** duplicate API call code (use API services)
6. **DO NOT** use inline styles
7. **DO NOT** import Material-UI directly (use wrappers from `/shared/ui/`)
8. **DO NOT** store secrets in localStorage
9. **DO NOT** use `any` type unnecessarily
10. **DO NOT** touch `frontend/` directory (deprecated Angular app)

---

## Development Workflow

1. **Before work:**
   - Pull latest from main
   - Review related components

2. **During:**
   - Follow these guidelines
   - Use TypeScript strict mode
   - Run linter: `npm run lint`

3. **Before commit:**
   - Fix linter errors
   - Review changes
   - Test in browser

---

## Additional Resources

- See [BACKEND.md](BACKEND.md) for backend guidelines
- Main config: [CLAUDE.md](../CLAUDE.md)
