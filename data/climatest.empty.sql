--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: agg_day; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.agg_day (
    id integer NOT NULL,
    start_dat timestamp with time zone NOT NULL,
    duration_sum integer NOT NULL,
    qa_modifications integer NOT NULL,
    qa_incidents integer NOT NULL,
    qa_check_done boolean NOT NULL,
    j jsonb NOT NULL,
    poste_id_id integer NOT NULL
);


ALTER TABLE public.agg_day OWNER TO postgres;

--
-- Name: agg_day_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.agg_day_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.agg_day_id_seq OWNER TO postgres;

--
-- Name: agg_day_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.agg_day_id_seq OWNED BY public.agg_day.id;


--
-- Name: agg_global; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.agg_global (
    id integer NOT NULL,
    start_dat timestamp with time zone NOT NULL,
    duration_sum integer NOT NULL,
    qa_modifications integer NOT NULL,
    qa_incidents integer NOT NULL,
    qa_check_done boolean NOT NULL,
    j jsonb NOT NULL,
    poste_id_id integer NOT NULL
);


ALTER TABLE public.agg_global OWNER TO postgres;

--
-- Name: agg_global_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.agg_global_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.agg_global_id_seq OWNER TO postgres;

--
-- Name: agg_global_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.agg_global_id_seq OWNED BY public.agg_global.id;


--
-- Name: agg_hour; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.agg_hour (
    id integer NOT NULL,
    start_dat timestamp with time zone NOT NULL,
    duration_sum integer NOT NULL,
    qa_modifications integer NOT NULL,
    qa_incidents integer NOT NULL,
    qa_check_done boolean NOT NULL,
    j jsonb NOT NULL,
    poste_id_id integer NOT NULL
);


ALTER TABLE public.agg_hour OWNER TO postgres;

--
-- Name: agg_hour_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.agg_hour_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.agg_hour_id_seq OWNER TO postgres;

--
-- Name: agg_hour_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.agg_hour_id_seq OWNED BY public.agg_hour.id;


--
-- Name: agg_month; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.agg_month (
    id integer NOT NULL,
    start_dat timestamp with time zone NOT NULL,
    duration_sum integer NOT NULL,
    qa_modifications integer NOT NULL,
    qa_incidents integer NOT NULL,
    qa_check_done boolean NOT NULL,
    j jsonb NOT NULL,
    poste_id_id integer NOT NULL
);


ALTER TABLE public.agg_month OWNER TO postgres;

--
-- Name: agg_month_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.agg_month_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.agg_month_id_seq OWNER TO postgres;

--
-- Name: agg_month_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.agg_month_id_seq OWNED BY public.agg_month.id;


--
-- Name: agg_year; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.agg_year (
    id integer NOT NULL,
    start_dat timestamp with time zone NOT NULL,
    duration_sum integer NOT NULL,
    qa_modifications integer NOT NULL,
    qa_incidents integer NOT NULL,
    qa_check_done boolean NOT NULL,
    j jsonb NOT NULL,
    poste_id_id integer NOT NULL
);


ALTER TABLE public.agg_year OWNER TO postgres;

--
-- Name: agg_year_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.agg_year_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.agg_year_id_seq OWNER TO postgres;

--
-- Name: agg_year_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.agg_year_id_seq OWNED BY public.agg_year.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: exclusion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exclusion (
    id integer NOT NULL,
    start_dat timestamp with time zone NOT NULL,
    end_dat timestamp with time zone NOT NULL,
    value jsonb NOT NULL,
    poste_id_id integer NOT NULL,
    type_instrument_id integer NOT NULL
);


ALTER TABLE public.exclusion OWNER TO postgres;

--
-- Name: exclusion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exclusion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exclusion_id_seq OWNER TO postgres;

--
-- Name: exclusion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exclusion_id_seq OWNED BY public.exclusion.id;


--
-- Name: obs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.obs (
    id integer NOT NULL,
    start_dat timestamp with time zone NOT NULL,
    stop_dat timestamp with time zone NOT NULL,
    duration integer NOT NULL,
    qa_modifications integer NOT NULL,
    qa_incidents integer NOT NULL,
    qa_check_done boolean NOT NULL,
    j jsonb NOT NULL,
    j_agg jsonb NOT NULL,
    poste_id_id integer NOT NULL
);


ALTER TABLE public.obs OWNER TO postgres;

--
-- Name: obs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.obs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.obs_id_seq OWNER TO postgres;

--
-- Name: obs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.obs_id_seq OWNED BY public.obs.id;


--
-- Name: poste; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.poste (
    id integer NOT NULL,
    meteor character varying(10) NOT NULL,
    fuseau smallint NOT NULL,
    meteofr character varying(10),
    cas_gestion_extreme smallint NOT NULL,
    agg_min_extreme character varying(1) NOT NULL,
    lock_calculus smallint,
    title character varying(50),
    owner character varying(50),
    email character varying(50),
    phone character varying(50),
    address character varying(50),
    zip character varying(10),
    city character varying(50),
    country character varying(50),
    latitude double precision,
    longitude double precision,
    start_dat timestamp with time zone,
    stop_dat timestamp with time zone,
    comment text
);


ALTER TABLE public.poste OWNER TO postgres;

--
-- Name: poste_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.poste_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.poste_id_seq OWNER TO postgres;

--
-- Name: poste_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.poste_id_seq OWNED BY public.poste.id;


--
-- Name: type_instrument; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.type_instrument (
    id integer NOT NULL,
    name character varying(10) NOT NULL,
    model_value jsonb NOT NULL
);


ALTER TABLE public.type_instrument OWNER TO postgres;

--
-- Name: type_instrument_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.type_instrument_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.type_instrument_id_seq OWNER TO postgres;

--
-- Name: type_instrument_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.type_instrument_id_seq OWNED BY public.type_instrument.id;


--
-- Name: agg_day id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_day ALTER COLUMN id SET DEFAULT nextval('public.agg_day_id_seq'::regclass);


--
-- Name: agg_global id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_global ALTER COLUMN id SET DEFAULT nextval('public.agg_global_id_seq'::regclass);


--
-- Name: agg_hour id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_hour ALTER COLUMN id SET DEFAULT nextval('public.agg_hour_id_seq'::regclass);


--
-- Name: agg_month id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_month ALTER COLUMN id SET DEFAULT nextval('public.agg_month_id_seq'::regclass);


--
-- Name: agg_year id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_year ALTER COLUMN id SET DEFAULT nextval('public.agg_year_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: exclusion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exclusion ALTER COLUMN id SET DEFAULT nextval('public.exclusion_id_seq'::regclass);


--
-- Name: obs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.obs ALTER COLUMN id SET DEFAULT nextval('public.obs_id_seq'::regclass);


--
-- Name: poste id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.poste ALTER COLUMN id SET DEFAULT nextval('public.poste_id_seq'::regclass);


--
-- Name: type_instrument id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.type_instrument ALTER COLUMN id SET DEFAULT nextval('public.type_instrument_id_seq'::regclass);


--
-- Data for Name: agg_day; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agg_day (id, start_dat, duration_sum, qa_modifications, qa_incidents, qa_check_done, j, poste_id_id) FROM stdin;
\.


--
-- Data for Name: agg_global; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agg_global (id, start_dat, duration_sum, qa_modifications, qa_incidents, qa_check_done, j, poste_id_id) FROM stdin;
\.


--
-- Data for Name: agg_hour; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agg_hour (id, start_dat, duration_sum, qa_modifications, qa_incidents, qa_check_done, j, poste_id_id) FROM stdin;
\.


--
-- Data for Name: agg_month; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agg_month (id, start_dat, duration_sum, qa_modifications, qa_incidents, qa_check_done, j, poste_id_id) FROM stdin;
\.


--
-- Data for Name: agg_year; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agg_year (id, start_dat, duration_sum, qa_modifications, qa_incidents, qa_check_done, j, poste_id_id) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add poste	1	add_poste
2	Can change poste	1	change_poste
3	Can delete poste	1	delete_poste
4	Can view poste	1	view_poste
5	Can add type instrument	2	add_typeinstrument
6	Can change type instrument	2	change_typeinstrument
7	Can delete type instrument	2	delete_typeinstrument
8	Can view type instrument	2	view_typeinstrument
9	Can add exclusion	3	add_exclusion
10	Can change exclusion	3	change_exclusion
11	Can delete exclusion	3	delete_exclusion
12	Can view exclusion	3	view_exclusion
13	Can add observation	4	add_observation
14	Can change observation	4	change_observation
15	Can delete observation	4	delete_observation
16	Can view observation	4	view_observation
17	Can add agg_year	5	add_agg_year
18	Can change agg_year	5	change_agg_year
19	Can delete agg_year	5	delete_agg_year
20	Can view agg_year	5	view_agg_year
21	Can add agg_month	6	add_agg_month
22	Can change agg_month	6	change_agg_month
23	Can delete agg_month	6	delete_agg_month
24	Can view agg_month	6	view_agg_month
25	Can add agg_hour	7	add_agg_hour
26	Can change agg_hour	7	change_agg_hour
27	Can delete agg_hour	7	delete_agg_hour
28	Can view agg_hour	7	view_agg_hour
29	Can add agg_global	8	add_agg_global
30	Can change agg_global	8	change_agg_global
31	Can delete agg_global	8	delete_agg_global
32	Can view agg_global	8	view_agg_global
33	Can add agg_day	9	add_agg_day
34	Can change agg_day	9	change_agg_day
35	Can delete agg_day	9	delete_agg_day
36	Can view agg_day	9	view_agg_day
37	Can add log entry	10	add_logentry
38	Can change log entry	10	change_logentry
39	Can delete log entry	10	delete_logentry
40	Can view log entry	10	view_logentry
41	Can add permission	11	add_permission
42	Can change permission	11	change_permission
43	Can delete permission	11	delete_permission
44	Can view permission	11	view_permission
45	Can add group	12	add_group
46	Can change group	12	change_group
47	Can delete group	12	delete_group
48	Can view group	12	view_group
49	Can add user	13	add_user
50	Can change user	13	change_user
51	Can delete user	13	delete_user
52	Can view user	13	view_user
53	Can add content type	14	add_contenttype
54	Can change content type	14	change_contenttype
55	Can delete content type	14	delete_contenttype
56	Can view content type	14	view_contenttype
57	Can add session	15	add_session
58	Can change session	15	change_session
59	Can delete session	15	delete_session
60	Can view session	15	view_session
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$216000$6FWusffr32Kk$3o33xVh/IxwAzASFQKoeRN4JP670KRyJH9whLYSzG7E=	\N	t	nico				t	t	2021-03-20 18:31:59.967905+04
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	app	poste
2	app	typeinstrument
3	app	exclusion
4	app	observation
5	app	agg_year
6	app	agg_month
7	app	agg_hour
8	app	agg_global
9	app	agg_day
10	admin	logentry
11	auth	permission
12	auth	group
13	auth	user
14	contenttypes	contenttype
15	sessions	session
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2021-03-20 18:31:08.231963+04
2	auth	0001_initial	2021-03-20 18:31:08.270444+04
3	admin	0001_initial	2021-03-20 18:31:08.309995+04
4	admin	0002_logentry_remove_auto_add	2021-03-20 18:31:08.322152+04
5	admin	0003_logentry_add_action_flag_choices	2021-03-20 18:31:08.330576+04
6	app	0001_initial	2021-03-20 18:31:08.405676+04
7	contenttypes	0002_remove_content_type_name	2021-03-20 18:31:08.450921+04
8	auth	0002_alter_permission_name_max_length	2021-03-20 18:31:08.458773+04
9	auth	0003_alter_user_email_max_length	2021-03-20 18:31:08.466232+04
10	auth	0004_alter_user_username_opts	2021-03-20 18:31:08.475086+04
11	auth	0005_alter_user_last_login_null	2021-03-20 18:31:08.483123+04
12	auth	0006_require_contenttypes_0002	2021-03-20 18:31:08.485349+04
13	auth	0007_alter_validators_add_error_messages	2021-03-20 18:31:08.49308+04
14	auth	0008_alter_user_username_max_length	2021-03-20 18:31:08.503802+04
15	auth	0009_alter_user_last_name_max_length	2021-03-20 18:31:08.512056+04
16	auth	0010_alter_group_name_max_length	2021-03-20 18:31:08.52144+04
17	auth	0011_update_proxy_permissions	2021-03-20 18:31:08.534487+04
18	auth	0012_alter_user_first_name_max_length	2021-03-20 18:31:08.544574+04
19	sessions	0001_initial	2021-03-20 18:31:08.55081+04
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: exclusion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exclusion (id, start_dat, end_dat, value, poste_id_id, type_instrument_id) FROM stdin;
\.


--
-- Data for Name: obs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.obs (id, start_dat, stop_dat, duration, qa_modifications, qa_incidents, qa_check_done, j, j_agg, poste_id_id) FROM stdin;
\.


--
-- Data for Name: poste; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.poste (id, meteor, fuseau, meteofr, cas_gestion_extreme, agg_min_extreme, lock_calculus, title, owner, email, phone, address, zip, city, country, latitude, longitude, start_dat, stop_dat, comment) FROM stdin;
1	BBF015	4	MF	3	H	0	Bain Boeuf - MRU	Nicolas	nicolas@cuvillier.net	+230	CP B1	33701	BB	MRU	-20	-57	2021-02-09 10:42:18+04	2021-06-11 10:43:31+04	Hello
\.


--
-- Data for Name: type_instrument; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.type_instrument (id, name, model_value) FROM stdin;
1	Temp	{"dewpoint": "float", "out_temp": "float", "soiltemp": "float", "heatindex": "float", "windchill": "float"}
2	Humidite	{"humidity": "int"}
3	Pression	{"pressure": "float", "barometer": "float"}
4	Rain	{"rain": "int", "rain_rate": "float"}
5	Wind	{"wind": "int", "win_i": "int", "wind10": "int", "wind_dir": "int", "wind_i_dir": "int"}
6	Solar	{"etp": "int", "radiation": "float", "uv_indice": "int"}
7	Interieur	{"in_temp": "float", "in_humidity": "int"}
9	Divers	{"rx": "int", "voltage": "float"}
\.


--
-- Name: agg_day_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.agg_day_id_seq', 1, false);


--
-- Name: agg_global_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.agg_global_id_seq', 1, false);


--
-- Name: agg_hour_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.agg_hour_id_seq', 1, false);


--
-- Name: agg_month_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.agg_month_id_seq', 1, false);


--
-- Name: agg_year_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.agg_year_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 60, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 15, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 19, true);


--
-- Name: exclusion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exclusion_id_seq', 1, true);


--
-- Name: obs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.obs_id_seq', 1, true);


--
-- Name: poste_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.poste_id_seq', 1, true);


--
-- Name: type_instrument_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.type_instrument_id_seq', 6, true);


--
-- Name: agg_day agg_day_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_day
    ADD CONSTRAINT agg_day_pkey PRIMARY KEY (id);


--
-- Name: agg_day agg_day_poste_id_id_start_dat_00b87cda_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_day
    ADD CONSTRAINT agg_day_poste_id_id_start_dat_00b87cda_uniq UNIQUE (poste_id_id, start_dat);


--
-- Name: agg_global agg_global_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_global
    ADD CONSTRAINT agg_global_pkey PRIMARY KEY (id);


--
-- Name: agg_global agg_global_poste_id_id_start_dat_a8050771_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_global
    ADD CONSTRAINT agg_global_poste_id_id_start_dat_a8050771_uniq UNIQUE (poste_id_id, start_dat);


--
-- Name: agg_hour agg_hour_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_hour
    ADD CONSTRAINT agg_hour_pkey PRIMARY KEY (id);


--
-- Name: agg_hour agg_hour_poste_id_id_start_dat_2d84d322_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_hour
    ADD CONSTRAINT agg_hour_poste_id_id_start_dat_2d84d322_uniq UNIQUE (poste_id_id, start_dat);


--
-- Name: agg_month agg_month_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_month
    ADD CONSTRAINT agg_month_pkey PRIMARY KEY (id);


--
-- Name: agg_month agg_month_poste_id_id_start_dat_cda8f91f_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_month
    ADD CONSTRAINT agg_month_poste_id_id_start_dat_cda8f91f_uniq UNIQUE (poste_id_id, start_dat);


--
-- Name: agg_year agg_year_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_year
    ADD CONSTRAINT agg_year_pkey PRIMARY KEY (id);


--
-- Name: agg_year agg_year_poste_id_id_start_dat_3a52ed78_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_year
    ADD CONSTRAINT agg_year_poste_id_id_start_dat_3a52ed78_uniq UNIQUE (poste_id_id, start_dat);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: exclusion exclusion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exclusion
    ADD CONSTRAINT exclusion_pkey PRIMARY KEY (id);


--
-- Name: obs obs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.obs
    ADD CONSTRAINT obs_pkey PRIMARY KEY (id);


--
-- Name: obs obs_poste_id_id_stop_dat_bc1b7a47_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.obs
    ADD CONSTRAINT obs_poste_id_id_stop_dat_bc1b7a47_uniq UNIQUE (poste_id_id, stop_dat);


--
-- Name: poste poste_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.poste
    ADD CONSTRAINT poste_pkey PRIMARY KEY (id);


--
-- Name: type_instrument type_instrument_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.type_instrument
    ADD CONSTRAINT type_instrument_pkey PRIMARY KEY (id);


--
-- Name: agg_day_poste_id_id_1381ef7d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX agg_day_poste_id_id_1381ef7d ON public.agg_day USING btree (poste_id_id);


--
-- Name: agg_global_poste_id_id_cbee566d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX agg_global_poste_id_id_cbee566d ON public.agg_global USING btree (poste_id_id);


--
-- Name: agg_hour_poste_id_id_d41a680d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX agg_hour_poste_id_id_d41a680d ON public.agg_hour USING btree (poste_id_id);


--
-- Name: agg_month_poste_id_id_190a27df; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX agg_month_poste_id_id_190a27df ON public.agg_month USING btree (poste_id_id);


--
-- Name: agg_year_poste_id_id_5cda07ae; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX agg_year_poste_id_id_5cda07ae ON public.agg_year USING btree (poste_id_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: exclusion_poste_id_id_9c3f49fa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX exclusion_poste_id_id_9c3f49fa ON public.exclusion USING btree (poste_id_id);


--
-- Name: exclusion_type_instrument_id_807cc03e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX exclusion_type_instrument_id_807cc03e ON public.exclusion USING btree (type_instrument_id);


--
-- Name: obs_poste_id_id_2f7212d7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX obs_poste_id_id_2f7212d7 ON public.obs USING btree (poste_id_id);


--
-- Name: agg_day agg_day_poste_id_id_1381ef7d_fk_poste_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_day
    ADD CONSTRAINT agg_day_poste_id_id_1381ef7d_fk_poste_id FOREIGN KEY (poste_id_id) REFERENCES public.poste(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: agg_global agg_global_poste_id_id_cbee566d_fk_poste_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_global
    ADD CONSTRAINT agg_global_poste_id_id_cbee566d_fk_poste_id FOREIGN KEY (poste_id_id) REFERENCES public.poste(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: agg_hour agg_hour_poste_id_id_d41a680d_fk_poste_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_hour
    ADD CONSTRAINT agg_hour_poste_id_id_d41a680d_fk_poste_id FOREIGN KEY (poste_id_id) REFERENCES public.poste(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: agg_month agg_month_poste_id_id_190a27df_fk_poste_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_month
    ADD CONSTRAINT agg_month_poste_id_id_190a27df_fk_poste_id FOREIGN KEY (poste_id_id) REFERENCES public.poste(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: agg_year agg_year_poste_id_id_5cda07ae_fk_poste_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_year
    ADD CONSTRAINT agg_year_poste_id_id_5cda07ae_fk_poste_id FOREIGN KEY (poste_id_id) REFERENCES public.poste(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exclusion exclusion_poste_id_id_9c3f49fa_fk_poste_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exclusion
    ADD CONSTRAINT exclusion_poste_id_id_9c3f49fa_fk_poste_id FOREIGN KEY (poste_id_id) REFERENCES public.poste(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exclusion exclusion_type_instrument_id_807cc03e_fk_type_instrument_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exclusion
    ADD CONSTRAINT exclusion_type_instrument_id_807cc03e_fk_type_instrument_id FOREIGN KEY (type_instrument_id) REFERENCES public.type_instrument(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: obs obs_poste_id_id_2f7212d7_fk_poste_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.obs
    ADD CONSTRAINT obs_poste_id_id_2f7212d7_fk_poste_id FOREIGN KEY (poste_id_id) REFERENCES public.poste(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

