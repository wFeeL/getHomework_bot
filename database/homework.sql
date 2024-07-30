--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3 (Debian 16.3-1.pgdg120+1)
-- Dumped by pg_dump version 16.3 (Debian 16.3-1.pgdg120+1)

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

ALTER TABLE IF EXISTS ONLY public.weekday DROP CONSTRAINT IF EXISTS weekday_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.timetable DROP CONSTRAINT IF EXISTS timetable_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS telegram_id;
ALTER TABLE IF EXISTS ONLY public.teachers DROP CONSTRAINT IF EXISTS teachers_pkey;
ALTER TABLE IF EXISTS ONLY public.subject DROP CONSTRAINT IF EXISTS subject_pkey;
ALTER TABLE IF EXISTS ONLY public.schedule DROP CONSTRAINT IF EXISTS schedule_pkey;
ALTER TABLE IF EXISTS ONLY public.homework DROP CONSTRAINT IF EXISTS homework_pkey;
ALTER TABLE IF EXISTS public.users ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.timetable ALTER COLUMN id DROP DEFAULT;
DROP TABLE IF EXISTS public.weekday;
DROP SEQUENCE IF EXISTS public.users_id_seq;
DROP TABLE IF EXISTS public.users;
DROP SEQUENCE IF EXISTS public.timetable_id_seq;
DROP TABLE IF EXISTS public.timetable;
DROP TABLE IF EXISTS public.teachers;
DROP TABLE IF EXISTS public.subject;
DROP TABLE IF EXISTS public.schedule;
DROP TABLE IF EXISTS public.homework;
DROP SEQUENCE IF EXISTS public.homework_id_seq;
--
-- Name: homework_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.homework_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.homework_id_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: homework; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.homework (
    id integer DEFAULT nextval('public.homework_id_seq'::regclass) NOT NULL,
    subject_id integer,
    date date,
    description character varying,
    file_id character varying(360) DEFAULT 'None'::character varying
);


ALTER TABLE public.homework OWNER TO postgres;

--
-- Name: schedule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.schedule (
    id integer NOT NULL,
    weekday_id integer NOT NULL,
    subject_id integer,
    weight integer NOT NULL
);


ALTER TABLE public.schedule OWNER TO postgres;

--
-- Name: subject; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subject (
    id integer NOT NULL,
    name character varying,
    sticker character varying,
    value boolean DEFAULT false NOT NULL
);


ALTER TABLE public.subject OWNER TO postgres;

--
-- Name: teachers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teachers (
    id integer NOT NULL,
    name character varying NOT NULL,
    subject_id integer NOT NULL
);


ALTER TABLE public.teachers OWNER TO postgres;

--
-- Name: timetable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.timetable (
    id integer NOT NULL,
    "time" character varying(20)
);


ALTER TABLE public.timetable OWNER TO postgres;

--
-- Name: timetable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.timetable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.timetable_id_seq OWNER TO postgres;

--
-- Name: timetable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.timetable_id_seq OWNED BY public.timetable.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    telegram_id character varying(100),
    admin boolean DEFAULT false NOT NULL,
    username character varying(360)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: weekday; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.weekday (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.weekday OWNER TO postgres;

--
-- Name: timetable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.timetable ALTER COLUMN id SET DEFAULT nextval('public.timetable_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: homework; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.homework VALUES (365, 1, '2024-07-22', 'учить!!', 'AgACAgIAAxkBAAI9S2ac30Psbo9TqpnYc561SCeE9-xWAAJO3jEbbMPoSFgVKS-1e_bVAQADAgADcwADNQQ');
INSERT INTO public.homework VALUES (144, 4, '2023-12-30', 'дописать', 'None');
INSERT INTO public.homework VALUES (366, 2, '2024-07-22', 'sdfsdf', 'AgACAgIAAxkBAAI9hmac4cKtl6IcDm4e8OP9630LIJPFAAJX3jEbbMPoSBuZmg_T11fuAQADAgADcwADNQQ');
INSERT INTO public.homework VALUES (372, 1, '2024-07-30', 'UHASDIASDASD', 'AgACAgIAAxkBAAJFNGan3pB0Wd3qauitJ2U5M6_tPovmAAI04jEbJk1BSTIPbUOV7-v7AQADAgADcwADNQQ');
INSERT INTO public.homework VALUES (367, 3, '2024-07-22', 'jxigdfg', 'AgACAgIAAxkBAAI9kGac4dSt-rW00dyHEubr7CJU8lrbAAJZ3jEbbMPoSAUmdELjc4hrAQADAgADcwADNQQ');
INSERT INTO public.homework VALUES (368, 4, '2024-07-22', 'hhijk;l;;', 'AgACAgIAAxkBAAI9mmac4ewwiIvRJBBXk6dDzFQ9WiqKAAJa3jEbbMPoSG4ebacJJjeKAQADAgADcwADNQQ');
INSERT INTO public.homework VALUES (129, 12, '2023-12-19', 'принести сборник ОГЭ по физике, упражнение 17', 'None');
INSERT INTO public.homework VALUES (130, 11, '2023-12-18', 'старое дз: упражнение 177', 'None');
INSERT INTO public.homework VALUES (209, 8, '2024-02-03', 'прочитать 4 главу', 'None');
INSERT INTO public.homework VALUES (369, 5, '2024-07-21', 'hjhk', 'AgACAgIAAxkBAAI9mmac4ewwiIvRJBBXk6dDzFQ9WiqKAAJa3jEbbMPoSG4ebacJJjeKAQADAgADcwADNQQ');
INSERT INTO public.homework VALUES (276, 3, '2024-03-20', 'страница 101 вопросы 2, 3
страница 105 вопросы 1-3
написать определения: 
генная инженерия - 
клеточная инженерия - 
искусственный мутагенез -', 'None');
INSERT INTO public.homework VALUES (277, 12, '2024-04-03', 'учить конденсаты по конспекту; учебник - §47; варианты ОГЭ до конца', 'None');
INSERT INTO public.homework VALUES (59, 12, '2023-11-21', 'читать §20-21, принести сборник (подписать их) для внеурочки', 'None');
INSERT INTO public.homework VALUES (60, 2, '2023-11-21', '12.10, 12.12, 12.14 (все четные), будет ПРОВЕРКА.', 'None');
INSERT INTO public.homework VALUES (61, 11, '2023-11-20', 'упражнение 122 (письменно)', 'None');
INSERT INTO public.homework VALUES (62, 8, '2023-11-25', 'Выучить стихотворения:

1. «Во глубине сибирских руд…» (не из учебника)

2. «Памятник» (учебник стр. 183-184)

3. «Пущину» (мой первый друг, мой друг бесценный)', 'None');
INSERT INTO public.homework VALUES (126, 8, '2023-12-16', 'будем писать сочинение по произведению «Евгений Онегин»', 'None');
INSERT INTO public.homework VALUES (128, 1, '2023-12-19', 'страница 68 упражнение 2, 3, 4', 'None');
INSERT INTO public.homework VALUES (278, 12, '2024-04-09', 'пишем пробник по физике (4, 5, 6 уроки)', 'None');
INSERT INTO public.homework VALUES (279, 8, '2024-04-06', 'начать читать и принести книгу «Собачье сердце»', 'None');
INSERT INTO public.homework VALUES (280, 12, '2024-04-05', 'повторить §47-49, учить теорию', 'None');
INSERT INTO public.homework VALUES (364, 1, '2024-07-21', 'sdf', 'AgACAgIAAxkBAAI9kGac4dSt-rW00dyHEubr7CJU8lrbAAJZ3jEbbMPoSAUmdELjc4hrAQADAgADcwADNQQ');
INSERT INTO public.homework VALUES (370, 5, '2024-07-22', 'dfgdfgd', 'None');
INSERT INTO public.homework VALUES (340, 2, '2024-05-16', 'контрольная работа по алгебре в формате ОГЭ', 'None');
INSERT INTO public.homework VALUES (343, 2, '2024-06-16', 'asdasd', 'None');
INSERT INTO public.homework VALUES (341, 13, '2024-01-13', 'ВЫПУСКНОЙ 🎉', 'None');
INSERT INTO public.homework VALUES (346, 2, '2024-06-20', 'sdf', 'None');
INSERT INTO public.homework VALUES (357, 2, '2024-07-12', 'UAHSDUHASIDASd', 'None');
INSERT INTO public.homework VALUES (359, 2, '2024-07-11', 'f', 'None');
INSERT INTO public.homework VALUES (6, 6, '2023-09-01', 'Принести учебник.', 'None');
INSERT INTO public.homework VALUES (46, 3, '2023-11-11', '§ 6, 7; конспект читать', 'None');
INSERT INTO public.homework VALUES (1, 1, '2023-09-01', 'Принести учебник.', 'None');
INSERT INTO public.homework VALUES (2, 2, '2023-09-01', 'Принести учебник.', 'None');
INSERT INTO public.homework VALUES (3, 3, '2023-09-01', 'Принести учебник.', 'None');
INSERT INTO public.homework VALUES (5, 5, '2023-09-01', 'Принести учебник.', 'None');
INSERT INTO public.homework VALUES (4, 4, '2023-09-01', 'Принести учебник.', 'None');
INSERT INTO public.homework VALUES (7, 7, '2023-09-01', 'Принести учебник.', 'None');
INSERT INTO public.homework VALUES (8, 8, '2023-09-01', 'Принести учебник.', 'None');
INSERT INTO public.homework VALUES (9, 9, '2023-09-01', 'Принести учебник.', 'None');
INSERT INTO public.homework VALUES (10, 10, '2023-09-01', 'Принести учебник.', 'None');
INSERT INTO public.homework VALUES (11, 11, '2023-09-01', 'Принести учебник.', 'None');
INSERT INTO public.homework VALUES (12, 12, '2023-09-01', 'Принести учебник.', 'None');
INSERT INTO public.homework VALUES (13, 13, '2023-09-01', 'Принести учебник.', 'None');
INSERT INTO public.homework VALUES (14, 14, '2023-09-01', 'Принести учебник.', 'None');
INSERT INTO public.homework VALUES (29, 10, '2023-11-11', 'составить сравнительную характеристику гражданского общества и правового государства. 2 общих, не менее 3 различий', 'None');
INSERT INTO public.homework VALUES (28, 8, '2023-11-06', 'выучить монолог Чацкого «А судьи кто?..»


конспект статьи И. Гончарова «Мильон терзаний». 

1. Общая оценка комедии;
2. Гончаров о Фамусовском обществе;
3. Чацкий в оценке Гончарова.', 'None');
INSERT INTO public.homework VALUES (30, 8, '2023-11-08', 'подготовиться к тесту по комедии Грибоедова', 'None');
INSERT INTO public.homework VALUES (32, 5, '2023-11-07', 'знать пять формул площадей треугольников с доказательствами', 'None');
INSERT INTO public.homework VALUES (34, 5, '2023-11-09', '№5.5, 5.7, 5.17, 5.21', 'None');
INSERT INTO public.homework VALUES (35, 2, '2023-11-08', '10.1 (2,3,4)', 'None');
INSERT INTO public.homework VALUES (36, 12, '2023-11-08', 'читать параграф 17, на уроке будем решать задачи', 'None');
INSERT INTO public.homework VALUES (37, 1, '2023-11-09', 'дописать письмо (все по правилам написания); учить герундий; просмотреть план рассказа (neighbourhood)', 'None');
INSERT INTO public.homework VALUES (38, 12, '2023-11-10', 'будет работа по теории; номера из задачника: 1574, 1578, 1580, 1581.', 'None');
INSERT INTO public.homework VALUES (39, 8, '2023-11-15', 'сочинение на тему «Современная ли комедия Горе от ума?»', 'None');
INSERT INTO public.homework VALUES (41, 1, '2023-11-14', 'составить рассказы neighbourhood (основная задача использовать лексику страница 32);', 'None');
INSERT INTO public.homework VALUES (40, 2, '2023-11-10', '10.4, 10.8, 10.12, 10.16', 'None');
INSERT INTO public.homework VALUES (43, 7, '2023-11-11', 'принести тетрадь по обществознанию, истории и географии', 'None');
INSERT INTO public.homework VALUES (44, 11, '2023-11-11', 'упражнение 106', 'None');
INSERT INTO public.homework VALUES (45, 2, '2023-11-14', 'будет работа по графикам уравнений', 'None');
INSERT INTO public.homework VALUES (33, 12, '2023-11-14', 'знать все формулы по току; будет работа по теории', 'None');
INSERT INTO public.homework VALUES (49, 11, '2023-11-13', 'доделать 110 (будет проверка)', 'None');
INSERT INTO public.homework VALUES (50, 11, '2023-11-17', 'будет диктант', 'None');
INSERT INTO public.homework VALUES (52, 2, '2023-11-15', '11.4, 11.6', 'None');
INSERT INTO public.homework VALUES (53, 7, '2023-11-16', 'сравнительная характеристика западников и славянофилов страница 76, 78; 4 сходства и 1-2 различия.', 'None');
INSERT INTO public.homework VALUES (54, 2, '2023-11-17', '12.2, 12.4, 12.6, 12.8 (делаем ТОЛЬКО четные); будет проверка', 'None');
INSERT INTO public.homework VALUES (55, 12, '2023-11-17', '§20, выучить все формулы, №1643, 1645, 1647', 'None');
INSERT INTO public.homework VALUES (47, 10, '2023-11-23', 'сгруппироваться и представить партию; создать программу, почему за вас должны проголосовать?', 'None');
INSERT INTO public.homework VALUES (48, 4, '2023-11-18', 'зачет по географии на первых уроках', 'None');
INSERT INTO public.homework VALUES (56, 14, '2023-11-20', 'доделать классную работу; номера из листка 2. Al (д), Fe (б)', 'None');
INSERT INTO public.homework VALUES (57, 1, '2023-11-21', 'стр. 42 упр. 4, 5; стр. 43 упр. 6. Записать с переводом номер 6', 'None');
INSERT INTO public.homework VALUES (58, 5, '2023-11-23', 'прочитать §6 и примеры задач к нему, выучить таблицу на странице 52', 'None');
INSERT INTO public.homework VALUES (361, 1, '2024-07-15', 'gh', 'None');
INSERT INTO public.homework VALUES (362, 1, '2024-07-15', 'gdgfdg', 'None');
INSERT INTO public.homework VALUES (363, 1, '2024-07-15', 'dfgfdg', 'None');
INSERT INTO public.homework VALUES (63, 8, '2023-11-20', 'Из интернета списать анализ стихотворения:

1 Группа (до Миши Драгуна) - «Пророк»

2 Группа (начиная от Золотарева, заканчивая Парфентьевым) - «К Чаадаеву»

3 Группа (после Парфентьева) - «Я вас любил…»', 'None');
INSERT INTO public.homework VALUES (64, 7, '2023-11-21', 'записать повод к войне, этапы войны: таблица (этап, событие, результат), итог войны', 'None');
INSERT INTO public.homework VALUES (65, 12, '2023-11-28', 'внеурочка: заканчиваем первый вариант (пропускаем задачи, темы которых мы мы не проходили)', 'None');
INSERT INTO public.homework VALUES (66, 12, '2023-11-22', 'номера из задачника: 1633, 1643, 1652', 'None');
INSERT INTO public.homework VALUES (67, 1, '2023-11-23', '46 упражнение 3,4 (будет ПРОВЕРКА)', 'None');
INSERT INTO public.homework VALUES (68, 2, '2023-11-22', '12.16', 'None');
INSERT INTO public.homework VALUES (69, 12, '2023-11-24', 'повторить энергию (8 класс); номера из задачника: 1654, 1663, 1667', 'None');
INSERT INTO public.homework VALUES (70, 11, '2023-11-25', 'будет изложение', 'None');
INSERT INTO public.homework VALUES (71, 1, '2023-11-30', 'написать рассказ про себя, используя пункты плана (7-10 предложений). использовать used to', 'None');
INSERT INTO public.homework VALUES (72, 1, '2023-11-28', 'будет аудирование, принести только тетрадь', 'None');
INSERT INTO public.homework VALUES (74, 5, '2023-11-28', 'прочитать параграф про окружность, площадь круга', 'None');
INSERT INTO public.homework VALUES (73, 2, '2023-11-28', '13.2 будет проверка и самостоятельная работа', 'None');
INSERT INTO public.homework VALUES (75, 11, '2023-11-25', 'доделать упражнение 138', 'None');
INSERT INTO public.homework VALUES (76, 10, '2023-12-02', '1. Отличительные признаки политической партии.
2. Функции политической партии.
3. Признаки политических движений.
4. Сходства(не меньше 2) и различия(не меньше 3) политических партий и общественных движений(таблица)', 'None');
INSERT INTO public.homework VALUES (77, 11, '2023-11-27', 'упражнение 141', 'None');
INSERT INTO public.homework VALUES (78, 8, '2023-12-09', 'Девочки - выучить письмо Татьяны Онегину,

Мальчики - выучить письмо Онегина Татьяне;', 'None');
INSERT INTO public.homework VALUES (79, 14, '2023-11-27', '2.2, 5; на листочке Водород. Задачи и переходы; написать физические свойства H2', 'None');
INSERT INTO public.homework VALUES (80, 11, '2023-12-01', 'упражнение 153', 'None');
INSERT INTO public.homework VALUES (81, 3, '2023-11-29', 'Подготовиться к проверочной работе по теме: "Клетка".', 'None');
INSERT INTO public.homework VALUES (82, 12, '2023-11-29', 'номера из задачника: 1669, 1633, 1643;', 'None');
INSERT INTO public.homework VALUES (83, 2, '2023-11-29', 'решить примеры (фотка в политехе)', 'None');
INSERT INTO public.homework VALUES (84, 12, '2023-12-05', 'сделать 2 вариант из сборника ОГЭ', 'None');
INSERT INTO public.homework VALUES (86, 12, '2023-12-01', '§21-22; всем выучить теорию', 'None');
INSERT INTO public.homework VALUES (88, 5, '2023-11-30', 'читать и учить параграф 7. 7.7,  7.9. 7.13', 'None');
INSERT INTO public.homework VALUES (90, 5, '2023-12-07', 'знать доказательство в учебнике на странице 75; 7.15', 'None');
INSERT INTO public.homework VALUES (91, 11, '2023-12-02', 'упражнение 159; будет проверка', 'None');
INSERT INTO public.homework VALUES (92, 12, '2023-12-05', '22-23, упражнение 22 + задача', 'None');
INSERT INTO public.homework VALUES (93, 11, '2023-12-04', 'упражнение 160', 'None');
INSERT INTO public.homework VALUES (94, 4, '2023-12-09', 'задание в политехе (фотка)', 'None');
INSERT INTO public.homework VALUES (95, 14, '2023-12-04', 'написать физические свойства для О2; 7-63, 7-145 из листочка', 'None');
INSERT INTO public.homework VALUES (85, 1, '2023-12-05', 'на уроке будем писать рассказ по плану; учить лексику модуля', 'None');
INSERT INTO public.homework VALUES (96, 4, '2023-12-09', 'нужно дописать в ЭГП ЦР:
1. топливно-энергетический комплекс(уголь, торф, нефтеперерабатывающие заводы);
2. крупнейшие электростанции(ТЭС, АЭС, ГАЭС);
3. сельское хозяйство.

прошлое домашнее задание', 'None');
INSERT INTO public.homework VALUES (97, 11, '2023-12-08', 'упражнение 162', 'None');
INSERT INTO public.homework VALUES (98, 8, '2023-12-06', 'читать главу 7', 'None');
INSERT INTO public.homework VALUES (99, 14, '2023-12-11', '2.107', 'None');
INSERT INTO public.homework VALUES (100, 2, '2023-12-05', '14.6, 14.10', 'None');
INSERT INTO public.homework VALUES (101, 5, '2023-12-07', '8.7, 8.9, 8.11', 'None');
INSERT INTO public.homework VALUES (102, 12, '2023-12-08', 'в конце учебника (страница 338) задача 36, 37, 38.', 'None');
INSERT INTO public.homework VALUES (103, 2, '2023-12-08', '14.12, 14.14, 14.17', 'None');
INSERT INTO public.homework VALUES (104, 1, '2023-12-07', 'страница 52, упражнение 2,3,4; просмотреть аппендикс, написать перевод; все записи должны быть в тетради', 'None');
INSERT INTO public.homework VALUES (105, 7, '2023-12-09', 'конспект §15', 'None');
INSERT INTO public.homework VALUES (106, 5, '2023-12-12', '(если будет геометрия) 8.16, 8.19, 8.22.', 'None');
INSERT INTO public.homework VALUES (108, 11, '2023-12-09', 'упражнение 175', 'None');
INSERT INTO public.homework VALUES (110, 2, '2023-12-12', '14.20, 14.21', 'None');
INSERT INTO public.homework VALUES (111, 11, '2023-12-11', 'упражнение 176', 'None');
INSERT INTO public.homework VALUES (51, 8, '2023-11-18', 'учить 3 стихотворения (рассказываем подряд): 

1. К Чаадаеву (страница 160)

2. «Пророк…» (страница 166)

3. «Я вас любил…» (страница 175)', 'None');
INSERT INTO public.homework VALUES (113, 12, '2023-12-12', '§24-26, полугодовая контрольная работа в среду 20.12 (в основном задачи на динамику и закон сохранения); теорию выучить', 'None');
INSERT INTO public.homework VALUES (114, 8, '2023-12-13', 'конспект статьи Белинского «Статья о Пушкине» статья 8,9 в формате тезисы / содержание', 'None');
INSERT INTO public.homework VALUES (116, 12, '2023-12-12', 'не точная инфа:

сделать 3 вариант по физике', 'None');
INSERT INTO public.homework VALUES (117, 12, '2023-12-19', 'доделать 3 вариант и сделать 4 вариант ОГЭ по физике', 'None');
INSERT INTO public.homework VALUES (118, 12, '2023-12-13', 'упражнение 26; повторяем теорию', 'None');
INSERT INTO public.homework VALUES (119, 1, '2023-12-14', 'стр. 56 прогресс чек', 'None');
INSERT INTO public.homework VALUES (120, 1, '2023-12-12', 'страница 53 упражнение 1, 2, 3; составить 2 предложения к каждому прошедшему времени (8)', 'None');
INSERT INTO public.homework VALUES (121, 2, '2023-12-19', 'работа по алгебре в формате ОГЭ', 'None');
INSERT INTO public.homework VALUES (123, 12, '2023-12-20', 'контрольная работа по физике', 'None');
INSERT INTO public.homework VALUES (122, 5, '2023-12-14', 'будет работа по геометрии и мат. диктант', 'None');
INSERT INTO public.homework VALUES (124, 1, '2023-12-15', '56 №3, 4, 5', 'None');
INSERT INTO public.homework VALUES (127, 12, '2023-12-15', 'УЧИТЬ ФОРМУЛЫ; стр. 334 №5 - 7, 19.', 'None');
INSERT INTO public.homework VALUES (115, 11, '2023-12-16', 'упражнение 177', 'None');
INSERT INTO public.homework VALUES (125, 8, '2023-12-15', 'будет тест по произведению «Евгений Онегин»', 'None');
INSERT INTO public.homework VALUES (134, 14, '2023-12-18', 'написать физические свойства серы; 

дописать ОВР 4HNO3 + S = 2H2O + 4NO2 + SO2 (что окислитель, а что восстановитель)', 'None');
INSERT INTO public.homework VALUES (135, 11, '2023-12-22', 'упражнение 189', 'None');
INSERT INTO public.homework VALUES (136, 10, '2023-12-21', 'повторить местное самоуправление (мсу) и гражданское общество', 'None');
INSERT INTO public.homework VALUES (137, 12, '2023-12-26', 'доделать 4 вариант; 
как, она сказала сделать все варианты по физике ОГЭ в свободное время', 'None');
INSERT INTO public.homework VALUES (138, 1, '2023-12-21', 'написать первый и второй пункт плана', 'None');
INSERT INTO public.homework VALUES (139, 8, '2023-12-23', 'прочитать повесть Бэла (принести)', 'None');
INSERT INTO public.homework VALUES (141, 1, '2023-12-22', 'будет сборка тетрадей;

дочитать текст, страница 58 упражнение 5, страница 59 упражнение 6; поработать со словами - перевод и тд;

задание письменное', 'None');
INSERT INTO public.homework VALUES (142, 5, '2023-12-26', '13.22, 13.25, 13.29', 'None');
INSERT INTO public.homework VALUES (145, 8, '2023-12-27', 'прочитать рассказ «Томань»', 'None');
INSERT INTO public.homework VALUES (140, 7, '2024-01-09', 'написать в таблицу реформу «Реформа просвещения и печати»(1860 -1870 гг.); обязательные даты - 1863, 1864, 1865, 1870.

написать вывод к таблице', 'None');
INSERT INTO public.homework VALUES (146, 12, '2024-01-09', 'внеурочка будет; прочитать §27-29', 'None');
INSERT INTO public.homework VALUES (205, 8, '2024-01-31', 'прочитать 3 и 4 главу', 'None');
INSERT INTO public.homework VALUES (206, 2, '2024-01-31', '23.22, 23.28', 'None');
INSERT INTO public.homework VALUES (207, 12, '2024-02-06', 'решить 11, 12 вариант по физике', 'None');
INSERT INTO public.homework VALUES (208, 12, '2024-02-02', 'повторить всю тему колебания будет работа; §37, упр. 34', 'None');
INSERT INTO public.homework VALUES (147, 8, '2024-01-13', 'в следующей четверти рассказать стихотворения: 

1 часть: 
страница 258 стихотворение Родина; 
стихотворение Дума (первую или вторую часть) вторая часть начинается - мечты поэзии…
выбрать стихотворение из любовной лирики (речь о Лермонтове)
 
2 часть:
стихотворение Пророк страница 264;
стихотворение И скучно и грустно страница 273', 'None');
INSERT INTO public.homework VALUES (148, 4, '2024-01-13', 'доделать классную работу (номер 6,7 страница 125; дать характеристику природных условий Европейского Севера для жизни и быта человека)', 'None');
INSERT INTO public.homework VALUES (186, 12, '2024-01-30', 'решить 9-10 вариант по физике ОГЭ', 'None');
INSERT INTO public.homework VALUES (143, 10, '2024-01-13', '1. Отметить гипотезу, диспозицию и санкцию в примере (фотка в политехе)

для подробной информации обратиться к чату «Политех»

2. доделать классную работу (тест 1, тема: 8§ Роль права в жизни человека, общества и государства)', 'None');
INSERT INTO public.homework VALUES (150, 7, '2024-01-18', 'зачет по реформам', 'None');
INSERT INTO public.homework VALUES (151, 7, '2024-01-11', 'доделать историю; 23 §', 'None');
INSERT INTO public.homework VALUES (152, 1, '2024-01-11', 'стр. 64 №2, 63 №5; значения Future учить', 'None');
INSERT INTO public.homework VALUES (153, 5, '2024-01-10', '15.2', 'None');
INSERT INTO public.homework VALUES (154, 5, '2024-01-11', '15.20, 15.28, 15.32 (2)', 'None');
INSERT INTO public.homework VALUES (155, 8, '2024-01-13', 'прочитать княжна Мэри записи 13 мая - 29 мая (письменно); объяснить каждую дату (встретился с кем-то, сделал то-то - в двух словах)', 'None');
INSERT INTO public.homework VALUES (157, 1, '2024-01-16', 'ПОВТОРИТЬ: страница 20 упражнение 1 (образование прилагательное), страница 36 (образование существительных), страница 68 упражнение 1', 'None');
INSERT INTO public.homework VALUES (158, 1, '2024-01-12', 'повторить времена Future, будет работа', 'None');
INSERT INTO public.homework VALUES (159, 11, '2024-01-13', 'упражнение 202', 'None');
INSERT INTO public.homework VALUES (160, 11, '2024-01-15', 'доделать 209', 'None');
INSERT INTO public.homework VALUES (161, 3, '2024-01-17', 'доделать классную работу (до смерти); будет ср по синтезу', 'None');
INSERT INTO public.homework VALUES (162, 8, '2024-01-15', 'выписать кратко записи Мэри с 3 июня и до конца', 'None');
INSERT INTO public.homework VALUES (163, 8, '2024-01-20', 'учить 2 часть стихов: 

1. стихотворение «Пророк» страница 264;

2. стихотворение «И скучно и грустно…»страница 273', 'None');
INSERT INTO public.homework VALUES (164, 14, '2024-01-15', 'сдать лабораторную работу (с прошлой четверти)', 'None');
INSERT INTO public.homework VALUES (165, 14, '2024-01-22', '4.10 (в), 4.18', 'None');
INSERT INTO public.homework VALUES (166, 11, '2024-01-19', 'упражнение 215', 'None');
INSERT INTO public.homework VALUES (167, 8, '2024-01-22', 'конспект статьи Белинского «„Герой нашего времени“ Лермонтова». 

Примерный план конспекта: 

1. Общая хар-ка
2. Связь с другими произведениями
3. Образы персонажей', 'None');
INSERT INTO public.homework VALUES (168, 12, '2024-01-16', 'принести тетрадь для огэ; знать все формулы', 'None');
INSERT INTO public.homework VALUES (171, 2, '2024-01-17', '21.6, 21.8, 21.10, 21.12', 'None');
INSERT INTO public.homework VALUES (172, 12, '2024-01-23', 'доделать 7 вариант и сделать 8 вариант ОГЭ по физике; учить формулы', 'None');
INSERT INTO public.homework VALUES (173, 1, '2024-01-18', 'у 2 группы будет работа по словообразованию; ответы на 1,2 на вопросы (письменно) по 3 предложения; рассказы opinion essay должны быть в тетради', 'None');
INSERT INTO public.homework VALUES (174, 12, '2024-01-19', 'таблица 3 упражнение 29,  по рисунку 71', 'None');
INSERT INTO public.homework VALUES (175, 2, '2024-01-18', '22.2, 22.4, 22.6, 22.10, 22.12; будет мат. диктант по домашнему заданию', 'None');
INSERT INTO public.homework VALUES (187, 1, '2024-01-25', 'страница 72 упражнения 1-4 Progress check', 'None');
INSERT INTO public.homework VALUES (176, 7, '2024-01-18', 'доделать классную работу: написать лидеров и их деятельность', 'None');
INSERT INTO public.homework VALUES (177, 2, '2024-01-23', '22.14, 22.16, 22.18, 22.20', 'None');
INSERT INTO public.homework VALUES (170, 5, '2024-01-19', '15.36, 15.38, 15.40', 'None');
INSERT INTO public.homework VALUES (179, 12, '2024-01-23', 'будет 1 задача на уравнение гармонических колебаний; номера из задачника - 1741, 1743', 'None');
INSERT INTO public.homework VALUES (178, 11, '2024-01-20', 'упражнение 229; будет изложение', 'None');
INSERT INTO public.homework VALUES (180, 8, '2024-01-22', 'прочитать 1 главу «Мертвые души», знать содержание; будет тест', 'None');
INSERT INTO public.homework VALUES (181, 5, '2024-01-23', 'страница 141 доказать теорему о медианах в треугольнике через вектора; 16.12, 16.14, 16.17', 'None');
INSERT INTO public.homework VALUES (182, 10, '2024-01-27', '1. Составить схему правоохранительных органов РФ
2. стр 95; вопросы 3, 5, 7, 8, 9
3. Выучить таблицу (фотка в политехе)', 'None');
INSERT INTO public.homework VALUES (184, 11, '2024-01-26', 'упражнение 230', 'None');
INSERT INTO public.homework VALUES (185, 1, '2024-01-23', 'дописать сочинение, подготовить рассказ

!!! не точное дз', 'None');
INSERT INTO public.homework VALUES (188, 2, '2024-01-24', '22.26, 22.28, 22.40, 23.8', 'None');
INSERT INTO public.homework VALUES (189, 5, '2024-01-24', 'страница 141 доказать теорему о медианах в треугольнике через вектора; 16.12, 16.14, 16.17', 'None');
INSERT INTO public.homework VALUES (190, 3, '2024-01-24', 'работа по задачам', 'None');
INSERT INTO public.homework VALUES (191, 12, '2024-01-26', '§32-33; упражнение 31', 'None');
INSERT INTO public.homework VALUES (192, 8, '2024-01-31', 'написать сочинение заданным темам (фотка в политехе)', 'None');
INSERT INTO public.homework VALUES (193, 2, '2024-01-26', '22.41, 22.42, 23.12, 23.18; будет работа по алгебре в пятницу на 1 урок', 'None');
INSERT INTO public.homework VALUES (183, 7, '2024-01-25', 'будет зачет по таблице «три течения в народничестве»; написать таблицу (фотка в политехе)', 'None');
INSERT INTO public.homework VALUES (194, 5, '2024-01-26', '16.17; 16.20; 16.24', 'None');
INSERT INTO public.homework VALUES (196, 1, '2024-01-30', '1 группа: стр 72 1-4; 71 номер 6

2 группа: p. 70 ex. 1, 3, 6; знать правила написания письма', 'None');
INSERT INTO public.homework VALUES (197, 12, '2024-01-30', '§28-30', 'None');
INSERT INTO public.homework VALUES (199, 10, '2024-02-01', 'обществознание вместо истории; будет зачет по таблице из политеха', 'None');
INSERT INTO public.homework VALUES (200, 14, '2024-01-29', 'сдать лабораторную работу', 'None');
INSERT INTO public.homework VALUES (198, 3, '2024-02-03', 'будет работа размножению мейоз митоз', 'None');
INSERT INTO public.homework VALUES (201, 11, '2024-01-29', 'будет работа на придаточные', 'None');
INSERT INTO public.homework VALUES (202, 8, '2024-01-29', 'читать Гоголя, 2 главы', 'None');
INSERT INTO public.homework VALUES (203, 14, '2024-02-05', '4.39, 4.59', 'None');
INSERT INTO public.homework VALUES (204, 11, '2024-02-02', 'подготовиться к диктанту по упражнениям 227, 130', 'None');
INSERT INTO public.homework VALUES (210, 1, '2024-02-01', 'Страница 91 номера 3(с обоснованием), 5 и 6', 'None');
INSERT INTO public.homework VALUES (211, 5, '2024-02-06', '17.7, 17.9, 17.11, 17.15', 'None');
INSERT INTO public.homework VALUES (212, 11, '2024-02-03', 'упражнение 235, написать схемы к предложениям', 'None');
INSERT INTO public.homework VALUES (213, 1, '2024-02-06', 'подготовить устный рассказ по плану из политеха (волонтеры)', 'None');
INSERT INTO public.homework VALUES (214, 4, '2024-02-10', '§43-45 (урал) будет тест', 'None');
INSERT INTO public.homework VALUES (215, 10, '2024-02-10', 'выучить таблицу по конспекту', 'None');
INSERT INTO public.homework VALUES (216, 11, '2024-02-05', 'упражнение 240', 'None');
INSERT INTO public.homework VALUES (217, 11, '2024-02-09', 'доделать 239', 'None');
INSERT INTO public.homework VALUES (219, 12, '2024-02-07', 'будет контрольная работа по колебаниям', 'None');
INSERT INTO public.homework VALUES (221, 8, '2024-02-07', 'прочитать 6 главу, возможно будут ответы на вопросы', 'None');
INSERT INTO public.homework VALUES (223, 12, '2024-02-09', 'повторить конспект; §38-39', 'None');
INSERT INTO public.homework VALUES (222, 2, '2024-02-08', 'пишем ОГЭ. приходим к 10:00 в 413 кабинет (других уроков не будет). принести черную гелевую ручку.', 'None');
INSERT INTO public.homework VALUES (224, 11, '2024-02-10', 'упражнение 242', 'None');
INSERT INTO public.homework VALUES (252, 1, '2024-03-05', '2 группа: повторить фразовые глаголы, формулы страдательного залога, страница 104 упражнение 3, страница 95 упражнение 8, готовиться к тесту', 'None');
INSERT INTO public.homework VALUES (225, 12, '2024-02-13', '§38-39, 1257, 1258, 1259', 'None');
INSERT INTO public.homework VALUES (226, 11, '2024-02-14', 'УСТНОЕ СОБЕСЕДОВАНИЕ', 'None');
INSERT INTO public.homework VALUES (227, 10, '2024-02-13', 'зачет по талблице', 'None');
INSERT INTO public.homework VALUES (228, 8, '2024-02-12', 'дочитать конец 8 главы и прочитать 9 главу', 'None');
INSERT INTO public.homework VALUES (218, 14, '2024-02-12', 'Написать электронный баланс к 2 уравнениям:

1. HNO3 + P = H3PO4 + NO2 + H2O
2. H2SO4 + P = H3PO4 + SO2 + H2O

Номера с листочка: 5.8, 5.10', 'None');
INSERT INTO public.homework VALUES (229, 11, '2024-02-16', 'упражнение 243', 'None');
INSERT INTO public.homework VALUES (230, 8, '2024-02-17', 'прочитать 10 главу', 'None');
INSERT INTO public.homework VALUES (231, 12, '2024-02-13', '13, 14 вариант ОГЭ', 'None');
INSERT INTO public.homework VALUES (232, 12, '2024-02-20', '14 (до конца), 15, 16 вариант ОГЭ; будем решать на листочках задачи', 'None');
INSERT INTO public.homework VALUES (233, 1, '2024-02-15', '2 группа: страница 94, упражнение 2 (переделать предложения из active в passive), страница 148 упражнение 1', 'None');
INSERT INTO public.homework VALUES (220, 7, '2024-02-17', 'будет зачет по русско-турецкой войне', 'None');
INSERT INTO public.homework VALUES (235, 1, '2024-02-16', '1 группа: страница 95 упражнение 7, страница 100 упражнение 1, 2', 'None');
INSERT INTO public.homework VALUES (236, 2, '2024-02-16', '25.30, 25.33, 25.35', 'None');
INSERT INTO public.homework VALUES (239, 2, '2024-02-20', 'решить задачи (фотка в политехе)', 'None');
INSERT INTO public.homework VALUES (238, 14, '2024-02-19', 'Вариант 2 задание 2 из листочка классной работы;

Вариант 2 задания 2, 3, 4 из листочка контрольной работы;', 'None');
INSERT INTO public.homework VALUES (240, 11, '2024-02-19', 'упражнение 253', 'None');
INSERT INTO public.homework VALUES (254, 11, '2024-03-02', 'упражнение 268', 'None');
INSERT INTO public.homework VALUES (234, 1, '2024-02-20', '2 группа: страница 100 упражнение 1, 2, 3', 'None');
INSERT INTO public.homework VALUES (241, 11, '2024-02-26', 'упражнение 257', 'None');
INSERT INTO public.homework VALUES (242, 12, '2024-02-21', 'задачник: №1779-1788', 'None');
INSERT INTO public.homework VALUES (243, 1, '2024-02-27', '1 группа: 100 №5, 101 №3, 5', 'None');
INSERT INTO public.homework VALUES (244, 12, '2024-02-27', '17-18 вариант ОГЭ', 'None');
INSERT INTO public.homework VALUES (245, 1, '2024-02-27', '2 группа: страница 100 номер 1, 2, 3; страница 101 (culture corner) читать и раскрываем скобки, упражнение 3, 5 (по плану)', 'None');
INSERT INTO public.homework VALUES (246, 12, '2024-02-27', '§40-42 упражнение 37, 38', 'None');
INSERT INTO public.homework VALUES (247, 2, '2024-02-27', '27.7, 27.9, 27.11', 'None');
INSERT INTO public.homework VALUES (248, 14, '2024-02-26', 'пример 5 на раздаточном материале', 'None');
INSERT INTO public.homework VALUES (249, 11, '2024-03-01', 'упражнение 263', 'None');
INSERT INTO public.homework VALUES (250, 8, '2024-03-04', 'сочинение на тему смысл названия поэмы Гоголя «Мертвые Души»', 'None');
INSERT INTO public.homework VALUES (251, 12, '2024-03-01', 'выучить конспект; §42-43, упражнение 39, 40.

решить задачу: 

Определить скорость электрона, который движется в магнитном поле индукцией 2 * 10^-4 Тл, описывая окружность радиусом 6 см, если он пролетает перпендикулярно.', 'None');
INSERT INTO public.homework VALUES (257, 11, '2024-03-04', 'упражнение 264', 'None');
INSERT INTO public.homework VALUES (305, 1, '2024-04-19', 'f', 'None');
INSERT INTO public.homework VALUES (253, 12, '2024-03-06', 'решить задачу (фотка в политехе); §43-44, упражнение 41; выучить алгоритм', 'None');
INSERT INTO public.homework VALUES (262, 8, '2024-03-13', 'выучить стихотворения на выбор: 

1. страница 52 (ветер принес…) и страница 54 ( о я хочу…)

2. страница 53 (о весна без конца…)', 'None');
INSERT INTO public.homework VALUES (261, 12, '2024-03-12', '§45 упражнение 42', 'None');
INSERT INTO public.homework VALUES (255, 3, '2024-03-20', 'ср по изменчивости', 'None');
INSERT INTO public.homework VALUES (259, 7, '2024-03-07', 'будет зачет по последней таблице (реформаторы)', 'None');
INSERT INTO public.homework VALUES (263, 7, '2024-03-12', 'дать характеристику А3 как личности и государственного деятеля, страница 9 вопрос 2, 5, 7', 'None');
INSERT INTO public.homework VALUES (264, 11, '2024-03-11', 'упражнение 274', 'None');
INSERT INTO public.homework VALUES (260, 12, '2024-03-12', 'прорешать задания из вариантов сборника ОГЭ: 

вариант 13 - 14; 
вариант 14 - 14, 22; 
вариант 15 - 12; 
вариант 16 - 16; 
вариант 17 - 16; 
вариант 18 - 14.', 'None');
INSERT INTO public.homework VALUES (258, 14, '2024-03-11', 'общие свойства металла(реакции с кислотами и с щелочью), электронные паспорта, в виде конспекта «кристаллические решетки металлов» общая характеристика;

это надо знать и уметь делать

номера из листочка: 1.3, 1.4, 1.5, 1.6', 'None');
INSERT INTO public.homework VALUES (266, 9, '2024-03-12', 'написать ответ на первый вопрос (фотка в политехе)', 'None');
INSERT INTO public.homework VALUES (267, 14, '2024-03-18', 'номер из листочка - 8.46', 'None');
INSERT INTO public.homework VALUES (268, 5, '2024-03-12', '9.3,  9.5,  9.7,  9.16,  9.29(1)', 'None');
INSERT INTO public.homework VALUES (269, 5, '2024-03-13', 'ср по окружностям', 'None');
INSERT INTO public.homework VALUES (270, 12, '2024-03-13', 'контрольная работа', 'None');
INSERT INTO public.homework VALUES (271, 1, '2024-03-14', 'страница 106 упражнение 4, 5, 7', 'None');
INSERT INTO public.homework VALUES (273, 2, '2024-03-14', '29.3, 29.4, 29.7; будет ср на эту тему', 'None');
INSERT INTO public.homework VALUES (274, 11, '2024-04-05', 'упражнение 476', 'None');
INSERT INTO public.homework VALUES (256, 4, '2024-03-20', 'sdfsdf', 'None');
INSERT INTO public.homework VALUES (272, 8, '2024-04-03', 'выучить стихотворения (страница 67-69): 

1. ОБЯЗАТЕЛЬНО - «Гой ты,  Русь, моя родная…»

2. На выбор - «Вот уж вечер…» ИЛИ «Край ты мой…» ИЛИ «Разбуди меня завтра рано…»', 'None');
INSERT INTO public.homework VALUES (281, 4, '2024-04-06', 'будет тест и зачет', 'None');
INSERT INTO public.homework VALUES (282, 7, '2024-04-09', 'будет тест по А3', 'None');
INSERT INTO public.homework VALUES (283, 1, '2024-04-11', 'пишем лексику и грамматику', 'None');
INSERT INTO public.homework VALUES (284, 1, '2024-04-16', 'страница 110-111 упражнения 4, 5, 11 по примеру; повторение тем к устному зачету: 
1. Neighbourhood
2. Internet 
3. Volunteering', 'None');
INSERT INTO public.homework VALUES (285, 2, '2024-04-05', 'работа на статистику у второй группы', 'None');
INSERT INTO public.homework VALUES (286, 11, '2024-04-11', 'пробник ОГЭ по русскому языку', 'None');
INSERT INTO public.homework VALUES (287, 2, '2024-04-05', '33.17 - 33.19', 'None');
INSERT INTO public.homework VALUES (288, 11, '2024-04-06', 'упражнение 291 доделать', 'None');
INSERT INTO public.homework VALUES (289, 11, '2024-04-08', 'упражнение 295 (1 часть)', 'None');
INSERT INTO public.homework VALUES (290, 14, '2024-04-15', 'написать свойства солей алюминия (взаимодействие со сложными, взаимодействие с водой: гидролиз, электролиз)', 'None');
INSERT INTO public.homework VALUES (291, 11, '2024-04-12', 'упражнение 298', 'None');
INSERT INTO public.homework VALUES (292, 12, '2024-04-16', 'устно будут спрашивать тех у кого 2/3 за тест; ср по конденсаторам (только формулы): §46, §50; решить задачу из политеха', 'None');
INSERT INTO public.homework VALUES (294, 3, '2024-04-20', 'ср по пройденным темам', 'None');
INSERT INTO public.homework VALUES (295, 11, '2024-04-15', 'упражнение 299 доделать; будет диктант и сборка тетрадей с домашними заданиями (298, 299)', 'None');
INSERT INTO public.homework VALUES (297, 1, '2024-04-16', 'придаточные условия, структура I wish', 'None');
INSERT INTO public.homework VALUES (306, 11, '2024-04-20', 'упражнение 313', 'None');
INSERT INTO public.homework VALUES (307, 5, '2024-04-23', '42.3, 42.4, 44.2, 44.3 (фотка номеров в политехе)', 'None');
INSERT INTO public.homework VALUES (299, 8, '2024-04-20', 'написать сочинение на одну из тем:

1. Почему Преображенский снова превратил шарикова в собаку?

2. Чудовищна или смешна история рассказанная Булгаковым?

3. Какие проблемы ставит Булгаков  в повести собачье сердце?', 'None');
INSERT INTO public.homework VALUES (300, 7, '2024-04-18', 'тест А3, будем подходить и отвечать оставшиеся вопросы', 'None');
INSERT INTO public.homework VALUES (301, 12, '2024-04-23', '30 вариант', 'None');
INSERT INTO public.homework VALUES (296, 11, '2024-04-19', 'словарный диктант', 'None');
INSERT INTO public.homework VALUES (304, 12, '2024-04-19', '§60-61', 'None');
INSERT INTO public.homework VALUES (308, 12, '2024-04-23', 'параграф 61 упражнение 52 (1, 2, 3)', 'None');
INSERT INTO public.homework VALUES (309, 11, '2024-04-22', 'упражнение 327 доделать и упражнение 331', 'None');
INSERT INTO public.homework VALUES (310, 14, '2024-04-22', 'лабораторная работа', 'None');
INSERT INTO public.homework VALUES (311, 11, '2024-04-26', 'упражнение 333, 336 доделать', 'None');
INSERT INTO public.homework VALUES (312, 8, '2024-04-24', 'дочитать и принести учебник', 'None');
INSERT INTO public.homework VALUES (313, 1, '2024-04-23', 'страница 112 упражнение 3, 4, 5', 'None');
INSERT INTO public.homework VALUES (314, 12, '2024-04-24', 'будет ср на расчеты энергии связи; определить энергию связи ядра P (30, 15) и N (14, 7); читать §62', 'None');
INSERT INTO public.homework VALUES (316, 14, '2024-04-24', 'сделать домашнюю  контрольную и дз', 'None');
INSERT INTO public.homework VALUES (317, 3, '2024-04-24', 'самостоятельная работа по пройденным темам', 'None');
INSERT INTO public.homework VALUES (318, 2, '2024-04-24', 'будет работа на прогрессии', 'None');
INSERT INTO public.homework VALUES (320, 2, '2024-04-26', 'мат. диктант', 'None');
INSERT INTO public.homework VALUES (321, 11, '2024-04-27', 'изложение, упражнение 339', 'None');
INSERT INTO public.homework VALUES (323, 3, '2024-05-04', 'ср по следующим темам: ЕО, адаптации, мутации', 'None');
INSERT INTO public.homework VALUES (324, 7, '2024-05-02', 'доделать классную работу (тест)', 'None');
INSERT INTO public.homework VALUES (325, 2, '2024-05-03', 'самостоятельная работа', 'None');
INSERT INTO public.homework VALUES (328, 11, '2024-05-04', 'упражнение 368 (1 часть)', 'None');
INSERT INTO public.homework VALUES (329, 11, '2024-05-06', 'контрольный диктант', 'None');
INSERT INTO public.homework VALUES (331, 8, '2024-05-04', 'на уроке будет пару вопросов по последнему произведению', 'None');
INSERT INTO public.homework VALUES (334, 11, '2024-05-10', 'доделать 370 упражнение', 'None');
INSERT INTO public.homework VALUES (335, 11, '2024-05-05', 'asjoij1oi23123', 'None');
INSERT INTO public.homework VALUES (332, 10, '2024-01-01', 'aushdasd', 'None');
INSERT INTO public.homework VALUES (326, 1, '2024-05-03', 'jdfngdfg', 'None');
INSERT INTO public.homework VALUES (303, 9, '2024-05-10', 'sdf', 'None');


--
-- Data for Name: schedule; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.schedule VALUES (8, 2, 15, 1);
INSERT INTO public.schedule VALUES (9, 2, 2, 2);
INSERT INTO public.schedule VALUES (10, 2, 7, 3);
INSERT INTO public.schedule VALUES (11, 2, 9, 4);
INSERT INTO public.schedule VALUES (12, 2, 17, 5);
INSERT INTO public.schedule VALUES (13, 2, 16, 6);
INSERT INTO public.schedule VALUES (14, 2, 18, 7);
INSERT INTO public.schedule VALUES (15, 3, 12, 1);
INSERT INTO public.schedule VALUES (16, 3, 12, 2);
INSERT INTO public.schedule VALUES (17, 3, 8, 3);
INSERT INTO public.schedule VALUES (18, 3, 3, 4);
INSERT INTO public.schedule VALUES (19, 3, 2, 5);
INSERT INTO public.schedule VALUES (20, 3, 2, 6);
INSERT INTO public.schedule VALUES (21, 4, 7, 1);
INSERT INTO public.schedule VALUES (22, 4, 7, 2);
INSERT INTO public.schedule VALUES (23, 4, 19, 3);
INSERT INTO public.schedule VALUES (24, 4, 19, 4);
INSERT INTO public.schedule VALUES (25, 4, 5, 5);
INSERT INTO public.schedule VALUES (28, 5, 11, 2);
INSERT INTO public.schedule VALUES (29, 5, 20, 3);
INSERT INTO public.schedule VALUES (30, 5, 20, 4);
INSERT INTO public.schedule VALUES (31, 5, 2, 5);
INSERT INTO public.schedule VALUES (32, 5, 12, 6);
INSERT INTO public.schedule VALUES (33, 5, 2, 7);
INSERT INTO public.schedule VALUES (34, 6, 4, 1);
INSERT INTO public.schedule VALUES (35, 6, 4, 2);
INSERT INTO public.schedule VALUES (36, 6, 3, 3);
INSERT INTO public.schedule VALUES (37, 6, 10, 4);
INSERT INTO public.schedule VALUES (38, 6, 11, 5);
INSERT INTO public.schedule VALUES (39, 6, 8, 6);
INSERT INTO public.schedule VALUES (2, 1, 14, 2);
INSERT INTO public.schedule VALUES (3, 1, 14, 3);
INSERT INTO public.schedule VALUES (4, 1, 13, 4);
INSERT INTO public.schedule VALUES (5, 1, 13, 5);
INSERT INTO public.schedule VALUES (6, 1, 11, 6);
INSERT INTO public.schedule VALUES (7, 1, 8, 7);
INSERT INTO public.schedule VALUES (1, 1, 14, 1);
INSERT INTO public.schedule VALUES (26, 4, 22, 7);
INSERT INTO public.schedule VALUES (40, 4, 5, 6);
INSERT INTO public.schedule VALUES (27, 5, NULL, 1);


--
-- Data for Name: subject; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.subject VALUES (15, 'Алгебра/Физика', '📈/💡', false);
INSERT INTO public.subject VALUES (16, 'Физика/Английский язык', '💡/🇺🇸', false);
INSERT INTO public.subject VALUES (17, 'Английский язык/Физика', '🇺🇸/💡', false);
INSERT INTO public.subject VALUES (18, 'Физика/Алгебра', '💡/📈', false);
INSERT INTO public.subject VALUES (20, 'Английский язык/Информатика', '🇺🇸/🖥', false);
INSERT INTO public.subject VALUES (22, 'Профориентация', '', false);
INSERT INTO public.subject VALUES (19, 'Информатика/Английский язык', '🖥/🇺🇸', false);
INSERT INTO public.subject VALUES (21, 'Нет урока', NULL, false);
INSERT INTO public.subject VALUES (1, 'Английский язык', '🇺🇸', true);
INSERT INTO public.subject VALUES (2, 'Алгебра', '📈', true);
INSERT INTO public.subject VALUES (3, 'Биология', '🧬', true);
INSERT INTO public.subject VALUES (4, 'География', '🗺', true);
INSERT INTO public.subject VALUES (5, 'Геометрия', '✏️', true);
INSERT INTO public.subject VALUES (6, 'Информатика', '🖥', true);
INSERT INTO public.subject VALUES (7, 'История', '📖', true);
INSERT INTO public.subject VALUES (8, 'Литература', '📚', true);
INSERT INTO public.subject VALUES (9, 'ОБЖ', '🌪', true);
INSERT INTO public.subject VALUES (10, 'Обществознание', '📊', true);
INSERT INTO public.subject VALUES (11, 'Русский язык', '🇷🇺', true);
INSERT INTO public.subject VALUES (12, 'Физика', '💡', true);
INSERT INTO public.subject VALUES (13, 'Физ-ра', '🏃', true);
INSERT INTO public.subject VALUES (14, 'Химия', '🧪', true);


--
-- Data for Name: teachers; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.teachers VALUES (1, 'Галина Павловна', 2);
INSERT INTO public.teachers VALUES (11, 'Людмила Валентиновна', 1);
INSERT INTO public.teachers VALUES (2, 'Галина Павловна', 5);
INSERT INTO public.teachers VALUES (3, 'Ольга Михайловна', 12);
INSERT INTO public.teachers VALUES (4, 'Ольга Леонидовна', 7);
INSERT INTO public.teachers VALUES (5, 'Ольга Леонидовна', 10);
INSERT INTO public.teachers VALUES (6, 'Ольга Леонидовна', 4);
INSERT INTO public.teachers VALUES (7, 'Виктория Григорьевна', 11);
INSERT INTO public.teachers VALUES (8, 'Виктория Григорьевна', 8);
INSERT INTO public.teachers VALUES (9, 'Марина Владимировна', 13);
INSERT INTO public.teachers VALUES (10, 'Майя Юрьевна', 14);
INSERT INTO public.teachers VALUES (12, 'Галина Павловна', 6);
INSERT INTO public.teachers VALUES (14, 'Елена Юрьевна', 3);
INSERT INTO public.teachers VALUES (13, 'Доля Валерьеновна', 9);


--
-- Data for Name: timetable; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.timetable VALUES (1, '8:30 - 9:10');
INSERT INTO public.timetable VALUES (2, '9:20 - 10:00');
INSERT INTO public.timetable VALUES (3, '10:20 - 11:00');
INSERT INTO public.timetable VALUES (4, '11:20 - 12:00');
INSERT INTO public.timetable VALUES (5, '12:20 - 13:00');
INSERT INTO public.timetable VALUES (6, '13:10 - 13:50');
INSERT INTO public.timetable VALUES (7, '14:00 - 14:40');
INSERT INTO public.timetable VALUES (8, '14:50 - 15:30');


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users VALUES (9, '6235035727', false, NULL);
INSERT INTO public.users VALUES (10, '5112866804', false, NULL);
INSERT INTO public.users VALUES (11, '2086714769', false, NULL);
INSERT INTO public.users VALUES (12, '1999387079', false, NULL);
INSERT INTO public.users VALUES (13, '1111185435', false, NULL);
INSERT INTO public.users VALUES (14, '1180999502', false, NULL);
INSERT INTO public.users VALUES (15, '1766982573', false, NULL);
INSERT INTO public.users VALUES (16, '1675631769', false, NULL);
INSERT INTO public.users VALUES (17, '1448748751', false, NULL);
INSERT INTO public.users VALUES (18, '1626828564', false, NULL);
INSERT INTO public.users VALUES (19, '5200616004', false, NULL);
INSERT INTO public.users VALUES (20, '1312071116', false, NULL);
INSERT INTO public.users VALUES (21, '1764292624', false, NULL);
INSERT INTO public.users VALUES (22, '5039417572', false, NULL);
INSERT INTO public.users VALUES (23, '5254125945', false, NULL);
INSERT INTO public.users VALUES (24, '1908202169', false, NULL);
INSERT INTO public.users VALUES (25, '1743455095', false, NULL);
INSERT INTO public.users VALUES (26, '1715469270', false, NULL);
INSERT INTO public.users VALUES (27, '1747223766', false, NULL);
INSERT INTO public.users VALUES (28, '1994450925', false, NULL);
INSERT INTO public.users VALUES (29, '5663880170', false, NULL);
INSERT INTO public.users VALUES (30, '2030064635', false, NULL);
INSERT INTO public.users VALUES (31, '5517895552', false, NULL);
INSERT INTO public.users VALUES (32, '1036096676', false, NULL);
INSERT INTO public.users VALUES (33, '1625926189', false, NULL);
INSERT INTO public.users VALUES (34, '1675000126', false, NULL);
INSERT INTO public.users VALUES (36, '5180932747', false, NULL);
INSERT INTO public.users VALUES (37, '6533619297', false, NULL);
INSERT INTO public.users VALUES (39, '1829378529', false, NULL);
INSERT INTO public.users VALUES (40, '5241465208', false, NULL);
INSERT INTO public.users VALUES (41, '5672724092', false, NULL);
INSERT INTO public.users VALUES (42, '5086225160', false, NULL);
INSERT INTO public.users VALUES (43, '5142273796', false, NULL);
INSERT INTO public.users VALUES (46, '5715030258', false, NULL);
INSERT INTO public.users VALUES (48, '7187699848', false, NULL);
INSERT INTO public.users VALUES (8, '6360506500', false, NULL);
INSERT INTO public.users VALUES (38, '1045003878', false, 'wkirk');
INSERT INTO public.users VALUES (53, '7444264138', false, 'wfeelz');
INSERT INTO public.users VALUES (54, '7391905497', false, 'sfanislavo');
INSERT INTO public.users VALUES (55, '403130114', false, 'TatyanaNS');
INSERT INTO public.users VALUES (35, '416966184', true, 'wfeels');


--
-- Data for Name: weekday; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.weekday VALUES (1, 'monday');
INSERT INTO public.weekday VALUES (2, 'tuesday');
INSERT INTO public.weekday VALUES (3, 'wednesday');
INSERT INTO public.weekday VALUES (4, 'thursday');
INSERT INTO public.weekday VALUES (5, 'friday');
INSERT INTO public.weekday VALUES (6, 'saturday');


--
-- Name: homework_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.homework_id_seq', 372, true);


--
-- Name: timetable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.timetable_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 55, true);


--
-- Name: homework homework_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.homework
    ADD CONSTRAINT homework_pkey PRIMARY KEY (id);


--
-- Name: schedule schedule_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schedule
    ADD CONSTRAINT schedule_pkey PRIMARY KEY (id);


--
-- Name: subject subject_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject
    ADD CONSTRAINT subject_pkey PRIMARY KEY (id);


--
-- Name: teachers teachers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teachers
    ADD CONSTRAINT teachers_pkey PRIMARY KEY (id);


--
-- Name: users telegram_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT telegram_id UNIQUE (telegram_id) INCLUDE (telegram_id);


--
-- Name: timetable timetable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.timetable
    ADD CONSTRAINT timetable_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: weekday weekday_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weekday
    ADD CONSTRAINT weekday_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

