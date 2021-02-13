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
    dat timestamp with time zone NOT NULL,
    last_rec_dat timestamp with time zone NOT NULL,
    duration integer NOT NULL,
    qa_modifications integer NOT NULL,
    qa_incidents integer NOT NULL,
    qa_check_done boolean NOT NULL,
    poste_id_id integer NOT NULL,
    barometer_avg numeric(5,1),
    barometer_duration integer,
    barometer_max numeric(5,1),
    barometer_max_time timestamp with time zone,
    barometer_min numeric(5,1),
    barometer_min_time timestamp with time zone,
    barometer_sum integer,
    dewpoint_max numeric(3,1),
    dewpoint_max_time timestamp with time zone,
    dewpoint_min numeric(3,1),
    dewpoint_min_time timestamp with time zone,
    humidity_duration timestamp with time zone,
    humidity_omm_max_time timestamp with time zone,
    heat_index_max numeric(3,1),
    heat_index_max_time timestamp with time zone,
    humidity_max smallint,
    humidity_max_time timestamp with time zone,
    humidity_min smallint,
    humidity_min_time smallint,
    in_humidity_max smallint,
    in_humidity_max_time timestamp with time zone,
    in_humidity_min smallint,
    in_humidity_min_time smallint,
    in_temp_max numeric(3,1),
    in_temp_max_time timestamp with time zone,
    in_temp_min numeric(3,1),
    in_temp_min_time timestamp with time zone,
    out_temp_avg numeric(3,1),
    out_temp_duration integer,
    out_temp_max numeric(3,1),
    out_temp_max_time timestamp with time zone,
    out_temp_min numeric(3,1),
    out_temp_min_time timestamp with time zone,
    out_temp_sum integer,
    rain_avg numeric(5,1),
    rain_duration integer,
    rain_rate_max numeric(5,1),
    rain_rate_max_time timestamp with time zone,
    rain_sum integer,
    rx_avg smallint,
    rx_duration integer,
    rx_max smallint,
    rx_max_time timestamp with time zone,
    rx_min smallint,
    rx_min_time timestamp with time zone,
    rx_sum integer,
    soil_temp_in_time timestamp with time zone,
    soil_temp_min numeric(3,1),
    radiation_max_time timestamp with time zone,
    radiation_min_time timestamp with time zone,
    humidity_avg smallint,
    barometer_omm_duration integer,
    voltage_max smallint,
    voltage_max_time timestamp with time zone,
    voltage_min smallint,
    voltage_min_time timestamp with time zone,
    barometer_omm_sum integer,
    out_temp_omm_duration integer,
    humidity_omm_max smallint,
    out_temp_omm_sum integer,
    radiation_duration integer,
    barometer_omm_avg numeric(5,1),
    humidity_omm_mesure smallint,
    uv_indice_max_time timestamp with time zone,
    out_temp_omm_avg numeric(3,1),
    radiation_max integer,
    out_temp_omm_mesure numeric(3,1),
    wind_max_time timestamp with time zone,
    windchill_min numeric(3,1),
    windchill_min_time timestamp with time zone,
    barometer_omm_mesure numeric(5,1),
    etp_sum numeric(7,3),
    humidity_omm_min smallint,
    humidity_omm_min_time smallint,
    humidity_sum smallint,
    radiation_min integer,
    radiation_sum integer,
    uv_indice_max smallint,
    wind_avg numeric(3,1),
    wind_duration integer,
    wind_i_avg numeric(3,1),
    wind_i_duration integer,
    wind_i_sum integer,
    wind_max numeric(5,1),
    wind_max_dir smallint,
    wind_sum integer
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
    dat timestamp with time zone NOT NULL,
    last_rec_dat timestamp with time zone NOT NULL,
    duration integer NOT NULL,
    qa_modifications integer NOT NULL,
    qa_incidents integer NOT NULL,
    qa_check_done boolean NOT NULL,
    poste_id_id integer NOT NULL,
    barometer_avg numeric(5,1),
    barometer_duration integer,
    barometer_max numeric(5,1),
    barometer_max_time timestamp with time zone,
    barometer_min numeric(5,1),
    barometer_min_time timestamp with time zone,
    barometer_sum integer,
    dewpoint_max numeric(3,1),
    dewpoint_max_time timestamp with time zone,
    dewpoint_min numeric(3,1),
    dewpoint_min_time timestamp with time zone,
    humidity_duration timestamp with time zone,
    humidity_omm_max_time timestamp with time zone,
    heat_index_max numeric(3,1),
    heat_index_max_time timestamp with time zone,
    humidity_max smallint,
    humidity_max_time timestamp with time zone,
    humidity_min smallint,
    humidity_min_time smallint,
    in_humidity_max smallint,
    in_humidity_max_time timestamp with time zone,
    in_humidity_min smallint,
    in_humidity_min_time smallint,
    in_temp_max numeric(3,1),
    in_temp_max_time timestamp with time zone,
    in_temp_min numeric(3,1),
    in_temp_min_time timestamp with time zone,
    out_temp_avg numeric(3,1),
    out_temp_duration integer,
    out_temp_max numeric(3,1),
    out_temp_max_time timestamp with time zone,
    out_temp_min numeric(3,1),
    out_temp_min_time timestamp with time zone,
    out_temp_sum integer,
    rain_avg numeric(5,1),
    rain_duration integer,
    rain_rate_max numeric(5,1),
    rain_rate_max_time timestamp with time zone,
    rain_sum integer,
    rx_avg smallint,
    rx_duration integer,
    rx_max smallint,
    rx_max_time timestamp with time zone,
    rx_min smallint,
    rx_min_time timestamp with time zone,
    rx_sum integer,
    soil_temp_in_time timestamp with time zone,
    soil_temp_min numeric(3,1),
    radiation_max_time timestamp with time zone,
    radiation_min_time timestamp with time zone,
    humidity_avg smallint,
    barometer_omm_duration integer,
    voltage_max smallint,
    voltage_max_time timestamp with time zone,
    voltage_min smallint,
    voltage_min_time timestamp with time zone,
    barometer_omm_sum integer,
    out_temp_omm_duration integer,
    humidity_omm_max smallint,
    out_temp_omm_sum integer,
    radiation_duration integer,
    barometer_omm_avg numeric(5,1),
    humidity_omm_mesure smallint,
    uv_indice_max_time timestamp with time zone,
    out_temp_omm_avg numeric(3,1),
    radiation_max integer,
    out_temp_omm_mesure numeric(3,1),
    wind_max_time timestamp with time zone,
    windchill_min numeric(3,1),
    windchill_min_time timestamp with time zone,
    barometer_omm_mesure numeric(5,1),
    etp_sum numeric(7,3),
    humidity_omm_min smallint,
    humidity_omm_min_time smallint,
    humidity_sum smallint,
    radiation_min integer,
    radiation_sum integer,
    uv_indice_max smallint,
    wind_avg numeric(3,1),
    wind_duration integer,
    wind_i_avg numeric(3,1),
    wind_i_duration integer,
    wind_i_sum integer,
    wind_max numeric(5,1),
    wind_max_dir smallint,
    wind_sum integer
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
    dat timestamp with time zone NOT NULL,
    last_rec_dat timestamp with time zone NOT NULL,
    duration integer NOT NULL,
    qa_modifications integer NOT NULL,
    qa_incidents integer NOT NULL,
    qa_check_done boolean NOT NULL,
    poste_id_id integer NOT NULL,
    barometer_avg numeric(5,1),
    barometer_duration integer,
    barometer_max numeric(5,1),
    barometer_max_time timestamp with time zone,
    barometer_min numeric(5,1),
    barometer_min_time timestamp with time zone,
    barometer_sum integer,
    dewpoint_max numeric(3,1),
    dewpoint_max_time timestamp with time zone,
    dewpoint_min numeric(3,1),
    dewpoint_min_time timestamp with time zone,
    humidity_duration timestamp with time zone,
    humidity_omm_max_time timestamp with time zone,
    heat_index_max numeric(3,1),
    heat_index_max_time timestamp with time zone,
    humidity_max smallint,
    humidity_max_time timestamp with time zone,
    humidity_min smallint,
    humidity_min_time smallint,
    in_humidity_max smallint,
    in_humidity_max_time timestamp with time zone,
    in_humidity_min smallint,
    in_humidity_min_time smallint,
    in_temp_max numeric(3,1),
    in_temp_max_time timestamp with time zone,
    in_temp_min numeric(3,1),
    in_temp_min_time timestamp with time zone,
    out_temp_avg numeric(3,1),
    out_temp_duration integer,
    out_temp_max numeric(3,1),
    out_temp_max_time timestamp with time zone,
    out_temp_min numeric(3,1),
    out_temp_min_time timestamp with time zone,
    out_temp_sum integer,
    rain_avg numeric(5,1),
    rain_duration integer,
    rain_rate_max numeric(5,1),
    rain_rate_max_time timestamp with time zone,
    rain_sum integer,
    rx_avg smallint,
    rx_duration integer,
    rx_max smallint,
    rx_max_time timestamp with time zone,
    rx_min smallint,
    rx_min_time timestamp with time zone,
    rx_sum integer,
    soil_temp_in_time timestamp with time zone,
    soil_temp_min numeric(3,1),
    radiation_max_time timestamp with time zone,
    radiation_min_time timestamp with time zone,
    humidity_avg smallint,
    barometer_omm_duration integer,
    voltage_max smallint,
    voltage_max_time timestamp with time zone,
    voltage_min smallint,
    voltage_min_time timestamp with time zone,
    barometer_omm_sum integer,
    out_temp_omm_duration integer,
    humidity_omm_max smallint,
    out_temp_omm_sum integer,
    radiation_duration integer,
    barometer_omm_avg numeric(5,1),
    humidity_omm_mesure smallint,
    uv_indice_max_time timestamp with time zone,
    out_temp_omm_avg numeric(3,1),
    radiation_max integer,
    out_temp_omm_mesure numeric(3,1),
    wind_max_time timestamp with time zone,
    windchill_min numeric(3,1),
    windchill_min_time timestamp with time zone,
    barometer_omm_mesure numeric(5,1),
    etp_sum numeric(7,3),
    humidity_omm_min smallint,
    humidity_omm_min_time smallint,
    humidity_sum smallint,
    radiation_min integer,
    radiation_sum integer,
    uv_indice_max smallint,
    wind_avg numeric(3,1),
    wind_duration integer,
    wind_i_avg numeric(3,1),
    wind_i_duration integer,
    wind_i_sum integer,
    wind_max numeric(5,1),
    wind_max_dir smallint,
    wind_sum integer
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
    dat timestamp with time zone NOT NULL,
    last_rec_dat timestamp with time zone NOT NULL,
    duration integer NOT NULL,
    qa_modifications integer NOT NULL,
    qa_incidents integer NOT NULL,
    qa_check_done boolean NOT NULL,
    poste_id_id integer NOT NULL,
    barometer_avg numeric(5,1),
    barometer_duration integer,
    barometer_max numeric(5,1),
    barometer_max_time timestamp with time zone,
    barometer_min numeric(5,1),
    barometer_min_time timestamp with time zone,
    barometer_sum integer,
    dewpoint_max numeric(3,1),
    dewpoint_max_time timestamp with time zone,
    dewpoint_min numeric(3,1),
    dewpoint_min_time timestamp with time zone,
    humidity_duration timestamp with time zone,
    humidity_omm_max_time timestamp with time zone,
    heat_index_max numeric(3,1),
    heat_index_max_time timestamp with time zone,
    humidity_max smallint,
    humidity_max_time timestamp with time zone,
    humidity_min smallint,
    humidity_min_time smallint,
    in_humidity_max smallint,
    in_humidity_max_time timestamp with time zone,
    in_humidity_min smallint,
    in_humidity_min_time smallint,
    in_temp_max numeric(3,1),
    in_temp_max_time timestamp with time zone,
    in_temp_min numeric(3,1),
    in_temp_min_time timestamp with time zone,
    out_temp_avg numeric(3,1),
    out_temp_duration integer,
    out_temp_max numeric(3,1),
    out_temp_max_time timestamp with time zone,
    out_temp_min numeric(3,1),
    out_temp_min_time timestamp with time zone,
    out_temp_sum integer,
    rain_avg numeric(5,1),
    rain_duration integer,
    rain_rate_max numeric(5,1),
    rain_rate_max_time timestamp with time zone,
    rain_sum integer,
    rx_avg smallint,
    rx_duration integer,
    rx_max smallint,
    rx_max_time timestamp with time zone,
    rx_min smallint,
    rx_min_time timestamp with time zone,
    rx_sum integer,
    soil_temp_in_time timestamp with time zone,
    soil_temp_min numeric(3,1),
    radiation_max_time timestamp with time zone,
    radiation_min_time timestamp with time zone,
    humidity_avg smallint,
    barometer_omm_duration integer,
    voltage_max smallint,
    voltage_max_time timestamp with time zone,
    voltage_min smallint,
    voltage_min_time timestamp with time zone,
    barometer_omm_sum integer,
    out_temp_omm_duration integer,
    humidity_omm_max smallint,
    out_temp_omm_sum integer,
    radiation_duration integer,
    barometer_omm_avg numeric(5,1),
    humidity_omm_mesure smallint,
    uv_indice_max_time timestamp with time zone,
    out_temp_omm_avg numeric(3,1),
    radiation_max integer,
    out_temp_omm_mesure numeric(3,1),
    wind_max_time timestamp with time zone,
    windchill_min numeric(3,1),
    windchill_min_time timestamp with time zone,
    barometer_omm_mesure numeric(5,1),
    etp_sum numeric(7,3),
    humidity_omm_min smallint,
    humidity_omm_min_time smallint,
    humidity_sum smallint,
    radiation_min integer,
    radiation_sum integer,
    uv_indice_max smallint,
    wind_avg numeric(3,1),
    wind_duration integer,
    wind_i_avg numeric(3,1),
    wind_i_duration integer,
    wind_i_sum integer,
    wind_max numeric(5,1),
    wind_max_dir smallint,
    wind_sum integer
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
    dat timestamp with time zone NOT NULL,
    last_rec_dat timestamp with time zone NOT NULL,
    duration integer NOT NULL,
    qa_modifications integer NOT NULL,
    qa_incidents integer NOT NULL,
    qa_check_done boolean NOT NULL,
    poste_id_id integer NOT NULL,
    barometer_avg numeric(5,1),
    barometer_duration integer,
    barometer_max numeric(5,1),
    barometer_max_time timestamp with time zone,
    barometer_min numeric(5,1),
    barometer_min_time timestamp with time zone,
    barometer_sum integer,
    dewpoint_max numeric(3,1),
    dewpoint_max_time timestamp with time zone,
    dewpoint_min numeric(3,1),
    dewpoint_min_time timestamp with time zone,
    humidity_duration timestamp with time zone,
    humidity_omm_max_time timestamp with time zone,
    heat_index_max numeric(3,1),
    heat_index_max_time timestamp with time zone,
    humidity_max smallint,
    humidity_max_time timestamp with time zone,
    humidity_min smallint,
    humidity_min_time smallint,
    in_humidity_max smallint,
    in_humidity_max_time timestamp with time zone,
    in_humidity_min smallint,
    in_humidity_min_time smallint,
    in_temp_max numeric(3,1),
    in_temp_max_time timestamp with time zone,
    in_temp_min numeric(3,1),
    in_temp_min_time timestamp with time zone,
    out_temp_avg numeric(3,1),
    out_temp_duration integer,
    out_temp_max numeric(3,1),
    out_temp_max_time timestamp with time zone,
    out_temp_min numeric(3,1),
    out_temp_min_time timestamp with time zone,
    out_temp_sum integer,
    rain_avg numeric(5,1),
    rain_duration integer,
    rain_rate_max numeric(5,1),
    rain_rate_max_time timestamp with time zone,
    rain_sum integer,
    rx_avg smallint,
    rx_duration integer,
    rx_max smallint,
    rx_max_time timestamp with time zone,
    rx_min smallint,
    rx_min_time timestamp with time zone,
    rx_sum integer,
    soil_temp_in_time timestamp with time zone,
    soil_temp_min numeric(3,1),
    radiation_max_time timestamp with time zone,
    radiation_min_time timestamp with time zone,
    humidity_avg smallint,
    barometer_omm_duration integer,
    voltage_max smallint,
    voltage_max_time timestamp with time zone,
    voltage_min smallint,
    voltage_min_time timestamp with time zone,
    barometer_omm_sum integer,
    out_temp_omm_duration integer,
    humidity_omm_max smallint,
    out_temp_omm_sum integer,
    radiation_duration integer,
    barometer_omm_avg numeric(5,1),
    humidity_omm_mesure smallint,
    uv_indice_max_time timestamp with time zone,
    out_temp_omm_avg numeric(3,1),
    radiation_max integer,
    out_temp_omm_mesure numeric(3,1),
    wind_max_time timestamp with time zone,
    windchill_min numeric(3,1),
    windchill_min_time timestamp with time zone,
    barometer_omm_mesure numeric(5,1),
    etp_sum numeric(7,3),
    humidity_omm_min smallint,
    humidity_omm_min_time smallint,
    humidity_sum smallint,
    radiation_min integer,
    radiation_sum integer,
    uv_indice_max smallint,
    wind_avg numeric(3,1),
    wind_duration integer,
    wind_i_avg numeric(3,1),
    wind_i_duration integer,
    wind_i_sum integer,
    wind_max numeric(5,1),
    wind_max_dir smallint,
    wind_sum integer
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
    start_x timestamp with time zone NOT NULL,
    end_x timestamp with time zone NOT NULL,
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
    dat timestamp with time zone NOT NULL,
    last_rec_dat timestamp with time zone NOT NULL,
    duration integer NOT NULL,
    qa_modifications integer NOT NULL,
    qa_incidents integer NOT NULL,
    qa_check_done boolean NOT NULL,
    poste_id_id integer NOT NULL,
    barometer numeric(5,1),
    barometer_max numeric(5,1),
    barometer_max_time timestamp with time zone,
    barometer_min numeric(5,1),
    barometer_min_time timestamp with time zone,
    dewpoint numeric(3,1),
    etp numeric(5,3),
    heat_index numeric(3,1),
    humidity smallint,
    humidity_max smallint,
    humidity_max_time timestamp with time zone,
    humidity_min smallint,
    humidity_min_time smallint,
    in_humidity smallint,
    in_temp numeric(3,1),
    radiation smallint,
    out_temp numeric(3,1),
    out_temp_max numeric(3,1),
    out_temp_max_time timestamp with time zone,
    out_temp_min numeric(3,1),
    out_temp_min_time timestamp with time zone,
    pressure numeric(5,1),
    rain_rate_max numeric(5,1),
    rain_rate_max_time timestamp with time zone,
    rain numeric(5,1),
    soil_temp numeric(3,1),
    soil_temp_min numeric(3,1),
    soil_temp_min_time timestamp with time zone,
    uv_indice smallint,
    wind_i_dir smallint,
    wind_dir smallint,
    rain_rate numeric(5,1),
    wind_max_dir smallint,
    wind_max_time timestamp with time zone,
    wind numeric(3,1),
    windchill numeric(3,1),
    rx smallint,
    voltage smallint,
    wind10 numeric(3,1),
    wind_i numeric(3,1),
    wind_max numeric(5,1)
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
    meteofr character varying(10),
    title character varying(50),
    cas_gestion_extreme character varying(1) NOT NULL,
    agg_min_extreme character varying(1),
    owner character varying(50),
    email character varying(50),
    phone character varying(50),
    address character varying(50),
    zip character varying(10),
    city character varying(50),
    country character varying(50),
    latitude double precision,
    longitude double precision,
    start timestamp with time zone,
    "end" timestamp with time zone,
    comment text,
    fuseau smallint NOT NULL
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
-- Name: type_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.type_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.type_data_id_seq OWNER TO postgres;

--
-- Name: type_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.type_data_id_seq OWNED BY public.type_instrument.id;


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

ALTER TABLE ONLY public.type_instrument ALTER COLUMN id SET DEFAULT nextval('public.type_data_id_seq'::regclass);


--
-- Data for Name: agg_day; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agg_day (id, dat, last_rec_dat, duration, qa_modifications, qa_incidents, qa_check_done, poste_id_id, barometer_avg, barometer_duration, barometer_max, barometer_max_time, barometer_min, barometer_min_time, barometer_sum, dewpoint_max, dewpoint_max_time, dewpoint_min, dewpoint_min_time, humidity_duration, humidity_omm_max_time, heat_index_max, heat_index_max_time, humidity_max, humidity_max_time, humidity_min, humidity_min_time, in_humidity_max, in_humidity_max_time, in_humidity_min, in_humidity_min_time, in_temp_max, in_temp_max_time, in_temp_min, in_temp_min_time, out_temp_avg, out_temp_duration, out_temp_max, out_temp_max_time, out_temp_min, out_temp_min_time, out_temp_sum, rain_avg, rain_duration, rain_rate_max, rain_rate_max_time, rain_sum, rx_avg, rx_duration, rx_max, rx_max_time, rx_min, rx_min_time, rx_sum, soil_temp_in_time, soil_temp_min, radiation_max_time, radiation_min_time, humidity_avg, barometer_omm_duration, voltage_max, voltage_max_time, voltage_min, voltage_min_time, barometer_omm_sum, out_temp_omm_duration, humidity_omm_max, out_temp_omm_sum, radiation_duration, barometer_omm_avg, humidity_omm_mesure, uv_indice_max_time, out_temp_omm_avg, radiation_max, out_temp_omm_mesure, wind_max_time, windchill_min, windchill_min_time, barometer_omm_mesure, etp_sum, humidity_omm_min, humidity_omm_min_time, humidity_sum, radiation_min, radiation_sum, uv_indice_max, wind_avg, wind_duration, wind_i_avg, wind_i_duration, wind_i_sum, wind_max, wind_max_dir, wind_sum) FROM stdin;
\.


--
-- Data for Name: agg_global; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agg_global (id, dat, last_rec_dat, duration, qa_modifications, qa_incidents, qa_check_done, poste_id_id, barometer_avg, barometer_duration, barometer_max, barometer_max_time, barometer_min, barometer_min_time, barometer_sum, dewpoint_max, dewpoint_max_time, dewpoint_min, dewpoint_min_time, humidity_duration, humidity_omm_max_time, heat_index_max, heat_index_max_time, humidity_max, humidity_max_time, humidity_min, humidity_min_time, in_humidity_max, in_humidity_max_time, in_humidity_min, in_humidity_min_time, in_temp_max, in_temp_max_time, in_temp_min, in_temp_min_time, out_temp_avg, out_temp_duration, out_temp_max, out_temp_max_time, out_temp_min, out_temp_min_time, out_temp_sum, rain_avg, rain_duration, rain_rate_max, rain_rate_max_time, rain_sum, rx_avg, rx_duration, rx_max, rx_max_time, rx_min, rx_min_time, rx_sum, soil_temp_in_time, soil_temp_min, radiation_max_time, radiation_min_time, humidity_avg, barometer_omm_duration, voltage_max, voltage_max_time, voltage_min, voltage_min_time, barometer_omm_sum, out_temp_omm_duration, humidity_omm_max, out_temp_omm_sum, radiation_duration, barometer_omm_avg, humidity_omm_mesure, uv_indice_max_time, out_temp_omm_avg, radiation_max, out_temp_omm_mesure, wind_max_time, windchill_min, windchill_min_time, barometer_omm_mesure, etp_sum, humidity_omm_min, humidity_omm_min_time, humidity_sum, radiation_min, radiation_sum, uv_indice_max, wind_avg, wind_duration, wind_i_avg, wind_i_duration, wind_i_sum, wind_max, wind_max_dir, wind_sum) FROM stdin;
\.


--
-- Data for Name: agg_hour; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agg_hour (id, dat, last_rec_dat, duration, qa_modifications, qa_incidents, qa_check_done, poste_id_id, barometer_avg, barometer_duration, barometer_max, barometer_max_time, barometer_min, barometer_min_time, barometer_sum, dewpoint_max, dewpoint_max_time, dewpoint_min, dewpoint_min_time, humidity_duration, humidity_omm_max_time, heat_index_max, heat_index_max_time, humidity_max, humidity_max_time, humidity_min, humidity_min_time, in_humidity_max, in_humidity_max_time, in_humidity_min, in_humidity_min_time, in_temp_max, in_temp_max_time, in_temp_min, in_temp_min_time, out_temp_avg, out_temp_duration, out_temp_max, out_temp_max_time, out_temp_min, out_temp_min_time, out_temp_sum, rain_avg, rain_duration, rain_rate_max, rain_rate_max_time, rain_sum, rx_avg, rx_duration, rx_max, rx_max_time, rx_min, rx_min_time, rx_sum, soil_temp_in_time, soil_temp_min, radiation_max_time, radiation_min_time, humidity_avg, barometer_omm_duration, voltage_max, voltage_max_time, voltage_min, voltage_min_time, barometer_omm_sum, out_temp_omm_duration, humidity_omm_max, out_temp_omm_sum, radiation_duration, barometer_omm_avg, humidity_omm_mesure, uv_indice_max_time, out_temp_omm_avg, radiation_max, out_temp_omm_mesure, wind_max_time, windchill_min, windchill_min_time, barometer_omm_mesure, etp_sum, humidity_omm_min, humidity_omm_min_time, humidity_sum, radiation_min, radiation_sum, uv_indice_max, wind_avg, wind_duration, wind_i_avg, wind_i_duration, wind_i_sum, wind_max, wind_max_dir, wind_sum) FROM stdin;
\.


--
-- Data for Name: agg_month; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agg_month (id, dat, last_rec_dat, duration, qa_modifications, qa_incidents, qa_check_done, poste_id_id, barometer_avg, barometer_duration, barometer_max, barometer_max_time, barometer_min, barometer_min_time, barometer_sum, dewpoint_max, dewpoint_max_time, dewpoint_min, dewpoint_min_time, humidity_duration, humidity_omm_max_time, heat_index_max, heat_index_max_time, humidity_max, humidity_max_time, humidity_min, humidity_min_time, in_humidity_max, in_humidity_max_time, in_humidity_min, in_humidity_min_time, in_temp_max, in_temp_max_time, in_temp_min, in_temp_min_time, out_temp_avg, out_temp_duration, out_temp_max, out_temp_max_time, out_temp_min, out_temp_min_time, out_temp_sum, rain_avg, rain_duration, rain_rate_max, rain_rate_max_time, rain_sum, rx_avg, rx_duration, rx_max, rx_max_time, rx_min, rx_min_time, rx_sum, soil_temp_in_time, soil_temp_min, radiation_max_time, radiation_min_time, humidity_avg, barometer_omm_duration, voltage_max, voltage_max_time, voltage_min, voltage_min_time, barometer_omm_sum, out_temp_omm_duration, humidity_omm_max, out_temp_omm_sum, radiation_duration, barometer_omm_avg, humidity_omm_mesure, uv_indice_max_time, out_temp_omm_avg, radiation_max, out_temp_omm_mesure, wind_max_time, windchill_min, windchill_min_time, barometer_omm_mesure, etp_sum, humidity_omm_min, humidity_omm_min_time, humidity_sum, radiation_min, radiation_sum, uv_indice_max, wind_avg, wind_duration, wind_i_avg, wind_i_duration, wind_i_sum, wind_max, wind_max_dir, wind_sum) FROM stdin;
\.


--
-- Data for Name: agg_year; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agg_year (id, dat, last_rec_dat, duration, qa_modifications, qa_incidents, qa_check_done, poste_id_id, barometer_avg, barometer_duration, barometer_max, barometer_max_time, barometer_min, barometer_min_time, barometer_sum, dewpoint_max, dewpoint_max_time, dewpoint_min, dewpoint_min_time, humidity_duration, humidity_omm_max_time, heat_index_max, heat_index_max_time, humidity_max, humidity_max_time, humidity_min, humidity_min_time, in_humidity_max, in_humidity_max_time, in_humidity_min, in_humidity_min_time, in_temp_max, in_temp_max_time, in_temp_min, in_temp_min_time, out_temp_avg, out_temp_duration, out_temp_max, out_temp_max_time, out_temp_min, out_temp_min_time, out_temp_sum, rain_avg, rain_duration, rain_rate_max, rain_rate_max_time, rain_sum, rx_avg, rx_duration, rx_max, rx_max_time, rx_min, rx_min_time, rx_sum, soil_temp_in_time, soil_temp_min, radiation_max_time, radiation_min_time, humidity_avg, barometer_omm_duration, voltage_max, voltage_max_time, voltage_min, voltage_min_time, barometer_omm_sum, out_temp_omm_duration, humidity_omm_max, out_temp_omm_sum, radiation_duration, barometer_omm_avg, humidity_omm_mesure, uv_indice_max_time, out_temp_omm_avg, radiation_max, out_temp_omm_mesure, wind_max_time, windchill_min, windchill_min_time, barometer_omm_mesure, etp_sum, humidity_omm_min, humidity_omm_min_time, humidity_sum, radiation_min, radiation_sum, uv_indice_max, wind_avg, wind_duration, wind_i_avg, wind_i_duration, wind_i_sum, wind_max, wind_max_dir, wind_sum) FROM stdin;
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
5	Can add agg_year	2	add_agg_year
6	Can change agg_year	2	change_agg_year
7	Can delete agg_year	2	delete_agg_year
8	Can view agg_year	2	view_agg_year
9	Can add agg_month	3	add_agg_month
10	Can change agg_month	3	change_agg_month
11	Can delete agg_month	3	delete_agg_month
12	Can view agg_month	3	view_agg_month
13	Can add agg_hour	4	add_agg_hour
14	Can change agg_hour	4	change_agg_hour
15	Can delete agg_hour	4	delete_agg_hour
16	Can view agg_hour	4	view_agg_hour
17	Can add agg_global	5	add_agg_global
18	Can change agg_global	5	change_agg_global
19	Can delete agg_global	5	delete_agg_global
20	Can view agg_global	5	view_agg_global
21	Can add agg_day	6	add_agg_day
22	Can change agg_day	6	change_agg_day
23	Can delete agg_day	6	delete_agg_day
24	Can view agg_day	6	view_agg_day
25	Can add observation	7	add_observation
26	Can change observation	7	change_observation
27	Can delete observation	7	delete_observation
28	Can view observation	7	view_observation
29	Can add log entry	8	add_logentry
30	Can change log entry	8	change_logentry
31	Can delete log entry	8	delete_logentry
32	Can view log entry	8	view_logentry
33	Can add permission	9	add_permission
34	Can change permission	9	change_permission
35	Can delete permission	9	delete_permission
36	Can view permission	9	view_permission
37	Can add group	10	add_group
38	Can change group	10	change_group
39	Can delete group	10	delete_group
40	Can view group	10	view_group
41	Can add user	11	add_user
42	Can change user	11	change_user
43	Can delete user	11	delete_user
44	Can view user	11	view_user
45	Can add content type	12	add_contenttype
46	Can change content type	12	change_contenttype
47	Can delete content type	12	delete_contenttype
48	Can view content type	12	view_contenttype
49	Can add session	13	add_session
50	Can change session	13	change_session
51	Can delete session	13	delete_session
52	Can view session	13	view_session
53	Can add type data	14	add_typedata
54	Can change type data	14	change_typedata
55	Can delete type data	14	delete_typedata
56	Can view type data	14	view_typedata
57	Can add exclusion	15	add_exclusion
58	Can change exclusion	15	change_exclusion
59	Can delete exclusion	15	delete_exclusion
60	Can view exclusion	15	view_exclusion
61	Can add type instrument	14	add_typeinstrument
62	Can change type instrument	14	change_typeinstrument
63	Can delete type instrument	14	delete_typeinstrument
64	Can view type instrument	14	view_typeinstrument
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$216000$PgJ1Nf9na6Gk$vb8UMeAdCzDS+e7Rf7iDjBFyJGlptYRennfWZFSILGk=	2021-02-09 17:18:15.305063+04	t	nico				t	t	2021-02-09 12:25:44.029674+04
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
1	2021-02-11 10:40:31.208106+04	2	test, id: 2	1	[{"added": {}}]	1	1
2	2021-02-11 11:34:14.927162+04	3	exclusion id: 3, poste: BBF015, id: 1, on type_instrument id: 1, name: Temp	1	[{"added": {}}]	15	1
3	2021-02-11 11:34:47.620284+04	4	exclusion id: 4, poste: BBF015, id: 1, on type_instrument id: 3, name: Rain	1	[{"added": {}}]	15	1
4	2021-02-11 11:41:51.657019+04	5	exclusion id: 5, poste: test, id: 2, on type_instrument id: 1, name: Temp	1	[{"added": {}}]	15	1
5	2021-02-11 11:42:28.257963+04	6	exclusion id: 6, poste: BBF015, id: 1, on type_instrument id: 1, name: Temp	1	[{"added": {}}]	15	1
6	2021-02-13 16:32:24.619324+04	1	BBF015, id: 1	2	[{"changed": {"fields": ["Nombre heure entre TU et heure fuseau"]}}]	1	1
7	2021-02-13 16:32:51.994952+04	3	test, id: 3	1	[{"added": {}}]	1	1
8	2021-02-13 16:33:00.446616+04	3	test, id: 3	3		1	1
9	2021-02-13 16:33:08.485012+04	2	test, id: 2	2	[{"changed": {"fields": ["Nombre heure entre TU et heure fuseau"]}}]	1	1
10	2021-02-13 16:34:41.06248+04	1	type_instrument id: 1, name: Temp	2	[{"changed": {"fields": ["JsonB"]}}]	14	1
11	2021-02-13 16:47:21.074212+04	8	observation id: 8, poste: BBF015, id: 1, on 2021-02-13 12:46:40+00:00	1	[{"added": {}}]	7	1
12	2021-02-13 16:49:48.56006+04	8	observation id: 8, poste: BBF015, id: 1, on 2021-02-13 12:46:40+00:00	3		7	1
13	2021-02-13 16:50:25.47355+04	9	observation id: 9, poste: BBF015, id: 1, on 2021-02-13 12:49:55+00:00	1	[{"added": {}}]	7	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	app	poste
2	app	agg_year
3	app	agg_month
4	app	agg_hour
5	app	agg_global
6	app	agg_day
7	app	observation
8	admin	logentry
9	auth	permission
10	auth	group
11	auth	user
12	contenttypes	contenttype
13	sessions	session
15	app	exclusion
14	app	typeinstrument
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	app	0001_initial	2021-02-09 12:24:09.430594+04
2	contenttypes	0001_initial	2021-02-09 12:24:20.020353+04
3	auth	0001_initial	2021-02-09 12:24:20.05103+04
4	admin	0001_initial	2021-02-09 12:24:20.094296+04
5	admin	0002_logentry_remove_auto_add	2021-02-09 12:24:20.106806+04
6	admin	0003_logentry_add_action_flag_choices	2021-02-09 12:24:20.114523+04
7	contenttypes	0002_remove_content_type_name	2021-02-09 12:24:20.137211+04
8	auth	0002_alter_permission_name_max_length	2021-02-09 12:24:20.146186+04
9	auth	0003_alter_user_email_max_length	2021-02-09 12:24:20.154923+04
10	auth	0004_alter_user_username_opts	2021-02-09 12:24:20.162787+04
11	auth	0005_alter_user_last_login_null	2021-02-09 12:24:20.171473+04
12	auth	0006_require_contenttypes_0002	2021-02-09 12:24:20.173631+04
13	auth	0007_alter_validators_add_error_messages	2021-02-09 12:24:20.18159+04
14	auth	0008_alter_user_username_max_length	2021-02-09 12:24:20.194701+04
15	auth	0009_alter_user_last_name_max_length	2021-02-09 12:24:20.202673+04
16	auth	0010_alter_group_name_max_length	2021-02-09 12:24:20.21275+04
17	auth	0011_update_proxy_permissions	2021-02-09 12:24:20.225609+04
18	auth	0012_alter_user_first_name_max_length	2021-02-09 12:24:20.233346+04
19	sessions	0001_initial	2021-02-09 12:24:20.240004+04
20	app	0002_exclusion_typedata	2021-02-09 13:04:42.228082+04
21	app	0003_auto_20210209_1221	2021-02-09 17:16:53.010931+04
22	app	0004_auto_20210209_1315	2021-02-09 17:16:53.854844+04
23	app	0005_auto_20210209_1316	2021-02-09 17:16:59.184688+04
24	app	0006_auto_20210209_1353	2021-02-09 17:53:41.963125+04
25	app	0007_auto_20210211_0536	2021-02-11 09:36:55.449108+04
26	app	0008_auto_20210211_0537	2021-02-11 09:37:36.703302+04
27	app	0009_auto_20210211_0539	2021-02-11 09:39:08.87305+04
28	app	0010_auto_20210211_0921	2021-02-11 13:21:46.6247+04
29	app	0011_auto_20210211_1231	2021-02-12 12:52:03.710011+04
30	app	0012_auto_20210212_0851	2021-02-12 12:52:03.786877+04
31	app	0013_auto_20210213_1230	2021-02-13 16:30:37.022897+04
32	app	0014_auto_20210213_1244	2021-02-13 16:44:33.523954+04
33	app	0015_auto_20210213_1245	2021-02-13 16:45:22.012672+04
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
vqk9c8pivv9zm2ujfve8viy9gnusrj3z	.eJxVjMsOwiAQAP-FsyFleVmP3v0GsguLVA0kpT0Z_92Q9KDXmcm8RcB9K2HvvIYliYtQ4vTLCOOT6xDpgfXeZGx1WxeSI5GH7fLWEr-uR_s3KNjL2EZOczaorJnQa2sdsM-A2qWskLzPGtDpSKijgZk8ZWvAnSewhjmD-HwB6d439g:1l9OLQ:A-ABoOxSoSIdZzm4QB1jMEOtIaNiRy6yYqrGdcr3o4k	2021-02-23 12:26:00.100705+04
iaknqoanuvxkqhm73hgduenvjh85bncd	.eJxVjMsOwiAQAP-FsyFleVmP3v0GsguLVA0kpT0Z_92Q9KDXmcm8RcB9K2HvvIYliYtQ4vTLCOOT6xDpgfXeZGx1WxeSI5GH7fLWEr-uR_s3KNjL2EZOczaorJnQa2sdsM-A2qWskLzPGtDpSKijgZk8ZWvAnSewhjmD-HwB6d439g:1l9SuF:V_eD45-bHSUy_9ML7WaLfsKHMdQChfvT1rnBz1T5U5I	2021-02-23 17:18:15.311859+04
\.


--
-- Data for Name: exclusion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exclusion (id, start_x, end_x, value, poste_id_id, type_instrument_id) FROM stdin;
4	2021-02-11 11:34:24+04	2100-12-21 04:00:00+04	{"rain_sum": 0}	1	3
5	2021-02-11 11:41:34+04	2100-12-21 04:00:00+04	{"station": 2}	2	1
6	2021-02-11 11:41:56+04	2021-02-01 11:42:06+04	{"actif": "none"}	1	1
3	2021-02-11 11:33:13+04	2100-12-21 04:00:00+04	{"temp_out": 123}	1	1
\.


--
-- Data for Name: obs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.obs (id, dat, last_rec_dat, duration, qa_modifications, qa_incidents, qa_check_done, poste_id_id, barometer, barometer_max, barometer_max_time, barometer_min, barometer_min_time, dewpoint, etp, heat_index, humidity, humidity_max, humidity_max_time, humidity_min, humidity_min_time, in_humidity, in_temp, radiation, out_temp, out_temp_max, out_temp_max_time, out_temp_min, out_temp_min_time, pressure, rain_rate_max, rain_rate_max_time, rain, soil_temp, soil_temp_min, soil_temp_min_time, uv_indice, wind_i_dir, wind_dir, rain_rate, wind_max_dir, wind_max_time, wind, windchill, rx, voltage, wind10, wind_i, wind_max) FROM stdin;
9	2021-02-13 16:49:55+04	2021-02-13 16:50:25.462786+04	300	0	0	f	1	1035.0	\N	\N	\N	\N	\N	0.000	\N	82	\N	\N	\N	\N	\N	\N	100	30.0	\N	\N	\N	\N	\N	\N	\N	0.0	\N	\N	\N	8	\N	80	0.0	\N	\N	5.0	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: poste; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.poste (id, meteor, meteofr, title, cas_gestion_extreme, agg_min_extreme, owner, email, phone, address, zip, city, country, latitude, longitude, start, "end", comment, fuseau) FROM stdin;
1	BBF015	MF	Bain Boeuf - MRU	3	H	Nicolas	nicolas@cuvillier.net	+230	CP B1	33701	BB	MRU	-20	-57	2021-02-09 10:42:18+04	2021-06-11 10:43:31+04	Hello	4
2	test	mf	test station	1	H	toto	toto@toto.com	123	earth	12345	city	country	0	0	2021-02-11 10:39:22+04	2021-02-11 10:40:13+04	comment	4
\.


--
-- Data for Name: type_instrument; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.type_instrument (id, name, model_value) FROM stdin;
2	Pression	{}
3	Rain	{}
4	Wind	{}
5	Solar	{}
6	Divers	{}
1	Temp	{"temp_out": "null"}
\.


--
-- Name: agg_day_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.agg_day_id_seq', 4, true);


--
-- Name: agg_global_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.agg_global_id_seq', 4, true);


--
-- Name: agg_hour_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.agg_hour_id_seq', 7, true);


--
-- Name: agg_month_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.agg_month_id_seq', 4, true);


--
-- Name: agg_year_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.agg_year_id_seq', 4, true);


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

SELECT pg_catalog.setval('public.auth_permission_id_seq', 64, true);


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

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 13, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 15, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 33, true);


--
-- Name: exclusion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exclusion_id_seq', 6, true);


--
-- Name: obs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.obs_id_seq', 9, true);


--
-- Name: poste_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.poste_id_seq', 3, true);


--
-- Name: type_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.type_data_id_seq', 6, true);


--
-- Name: agg_day agg_day_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_day
    ADD CONSTRAINT agg_day_pkey PRIMARY KEY (id);


--
-- Name: agg_global agg_global_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_global
    ADD CONSTRAINT agg_global_pkey PRIMARY KEY (id);


--
-- Name: agg_hour agg_hour_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_hour
    ADD CONSTRAINT agg_hour_pkey PRIMARY KEY (id);


--
-- Name: agg_month agg_month_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_month
    ADD CONSTRAINT agg_month_pkey PRIMARY KEY (id);


--
-- Name: agg_year agg_year_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agg_year
    ADD CONSTRAINT agg_year_pkey PRIMARY KEY (id);


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
-- Name: obs obs_poste_id_id_dat_8291c50e_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.obs
    ADD CONSTRAINT obs_poste_id_id_dat_8291c50e_uniq UNIQUE (poste_id_id, dat);


--
-- Name: poste poste_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.poste
    ADD CONSTRAINT poste_pkey PRIMARY KEY (id);


--
-- Name: type_instrument type_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.type_instrument
    ADD CONSTRAINT type_data_pkey PRIMARY KEY (id);


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
-- Name: exclusion_type_data_id_978f99c5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX exclusion_type_data_id_978f99c5 ON public.exclusion USING btree (type_instrument_id);


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

