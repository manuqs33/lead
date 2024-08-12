import { z } from 'zod';

const lettersOnly = /^[A-Za-zÀ-ÖØ-öø-ÿÑñ\s]+$/;
const phoneNumber = /^\+?\d+$/;
const lettersNumbers = /^[A-Za-zÀ-ÖØ-öø-ÿÑñ\s\d]+$/;



const PostSubjectSchema = z.object({
    id: z.number().optional(),
    name: z.string().max(100, {
        message: "El nombre de la materia debe tener menos de 100 caracteres",
    }).regex(lettersNumbers, {
        message: "El nombre de la materia solo puede contener letras y números",
    }),
    duration_in_months: z.number().int().min(1, {
        message: "La duración de la materia debe ser al menos 1 mes",
    }).max(12, {
        message: "La duración de la materia debe ser como máximo 12 meses",
    }).optional(),

    register_year: z.number().int().min(1990, {
        message: "El año de inscripción debe ser al menos 1990",
    }).max(2025, {
        message: "El año de inscripción debe ser como máximo 2025",
    }).optional(),
    times_taken: z.number().int().min(1, {
        message: "El número de veces de cursada debe ser al menos 1",
    }).max(10, {
        message: "Times taken must be max 10",
    }).optional(),
});

const PostDegreeSchema = z.object({
    id: z.number().optional(),
    name: z.string().max(100, {
        message: "El nombre de la carrera debe tener menos de 100 caracteres",
    }).regex(lettersOnly, {
        message: "El nombre de la carrera solo puede contener letras",
    }),
    subjects: z.array(PostSubjectSchema).optional(),
});

const PostLeadSchema = z.object({
    full_name: z.string().max(100, {
        message: "El nombre completo debe tener menos de 100 caracteres",
    }).regex(lettersOnly, {
        message: "El nombre completo solo puede contener letras",
    }),

    email: z.string().email({
        message: "Por favor ingrese un email válido",
    }).max(100, {
        message: "El email debe tener menos de 100 caracteres",
    }),

    address: z.string().max(100, {
        message: "La dirección debe tener menos de 100 caracteres",
    }).regex(lettersNumbers, {
        message: "La dirección solo puede contener letras y números",
    }).optional().or(z.literal('')),

    phone: z.string().max(20, {
        message: "El teléfono debe tener como máximo 20 caracteres",
    }).regex(phoneNumber, {
        message: "El teléfono puede empezar con + o número y continuar solo con números",
    }).optional().or(z.literal('')),

    degrees: z.array(PostDegreeSchema).optional(),
});

export { PostDegreeSchema, PostLeadSchema, PostSubjectSchema };