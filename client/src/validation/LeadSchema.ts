import { z } from 'zod';

const lettersOnly = /^[A-Za-zÀ-ÖØ-öø-ÿÑñ\s]+$/;
const phoneNumber = /^\+?\d+$/;
const lettersNumbers = /^[A-Za-zÀ-ÖØ-öø-ÿÑñ\s\d]+$/;



const PostSubjectSchema = z.object({
    id: z.number().optional(),

    name: z.string().max(100, {
        message: "El nombre de la materia debe tener menos de 100 caracteres",
    }).regex(lettersNumbers, {
        message: "El nombre de la materia es obligatorio y solo puede contener letras y números",
    }),

    duration_in_months: z.coerce.number()
    .int({message: "La duración de la materia debe ser un número entero"})
    .min(1, {
        message: "La duración de la materia debe ser un número, 1 como mínimo",
    })
    .max(12, {
        message: "La duración de la materia debe ser como máximo 12 meses",
    })
    .optional().or(z.literal('')).transform(value => value === '' ? undefined : value),

    register_year: z.coerce
    .number({message: "El año de inscripción es obligatorio y debe ser un número"})
    .int({message: "El año de inscripción debe ser un número entero"})
    .min(1990, {
        message: "El año de inscripción debe ser un número, 1990 como mínimo",
    })
    .max(2025, {
        message: "El año de inscripción debe ser como máximo 2025",
    }),

    times_taken: z.coerce.number()
    .int({message: "El número de veces que se cursó la materia debe ser un número entero"})
    .min(1, {
        message: "El número de veces que se cursó la materia debe ser al menos 1",
    }).max(10, {
        message: "El número de veces que se cursó la materia debe ser como máximo 10",
    }).optional().or(z.literal('')).transform(value => value === '' ? undefined : value),
});

const PostDegreeSchema = z.object({
    id: z.number().optional(),
    name: z.string().max(100, {
        message: "El nombre de la carrera debe tener menos de 100 caracteres",
    }).regex(lettersOnly, {
        message: "El nombre de la carrera es obligatorio y solo puede contener letras",
    }),
    subjects: z.array(PostSubjectSchema).optional(),
});

const PostLeadSchema = z.object({
    full_name: z.string().max(100, {
        message: "El nombre completo debe tener menos de 100 caracteres",
    }).regex(lettersOnly, {
        message: "El nombre completo es obligatorio y solo puede contener letras",
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
    }).optional().or(z.literal('')).transform(value => value === '' ? undefined : value),

    phone: z.string().max(20, {
        message: "El teléfono debe tener como máximo 20 caracteres",
    }).regex(phoneNumber, {
        message: "El teléfono puede empezar con + o número y continuar solo con números",
    }).optional().or(z.literal('')).transform(value => value === '' ? undefined : value),

    degrees: z.array(PostDegreeSchema).optional(),
});

export { PostDegreeSchema, PostLeadSchema, PostSubjectSchema };