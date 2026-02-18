CREATE TABLE public.statuses (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE public.priorities (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE public.lists (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    username TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL
);

CREATE TABLE public.tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,

    parent_task_id INTEGER
        REFERENCES public.tasks(id)
        ON DELETE CASCADE,

    user_id INTEGER NOT NULL
        REFERENCES public.users(id)
        ON DELETE CASCADE,

    list_id INTEGER
        REFERENCES public.lists(id)
        ON DELETE SET NULL,

    priority_id INTEGER
        REFERENCES public.priorities(id),

    status_id INTEGER
        REFERENCES public.statuses(id)
);

CREATE TABLE public.activity_log (
    id BIGSERIAL PRIMARY KEY,

    task_id INTEGER NOT NULL
        REFERENCES public.tasks(id)
        ON DELETE CASCADE,

    action TEXT NOT NULL,
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user ON public.tasks(user_id);
CREATE INDEX idx_tasks_status ON public.tasks(status_id);
CREATE INDEX idx_activity_task ON public.activity_log(task_id);
