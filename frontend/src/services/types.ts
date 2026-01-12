export interface Token {
  access_token: string;
  token_type: string;
}

// Based on backend/models.py UserCreate
export interface UserCreate {
  email: string;
  password: string;
  birth_date: string; // YYYY-MM-DD format
}

// Based on backend/models.py UserRead
export interface UserRead {
  id: number;
  email: string;
  birth_date: string;
  bio: string | null;
  image_filename: string | null;
  zodiac_sign_id: number | null;
  zodiac_sign_name: string | null;
}
