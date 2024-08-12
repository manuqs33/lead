import { z } from "zod";
import { PostLeadSchema } from "../validation/LeadSchema";
import { FormProvider, useForm, useFormContext } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { ReactNode } from "react";

/* export type CreateSubjectFromLead = z.infer<typeof PostSubjectSchema>

export type CreateDegreeFromLead = z.infer<typeof PostDegreeSchema> */

export type Lead = z.infer<typeof PostLeadSchema>

export const useFormLead = () =>
    useForm<Lead>({
        resolver: zodResolver(PostLeadSchema),
    });


export const FormProviderLead = ({
    children,
}: {
    children: ReactNode
}) => {
    const methods = useFormLead()
    return <FormProvider {...methods}>{children}</FormProvider>
}

export const useFormContextLead = () =>
    useFormContext<Lead>()


/* export const useFormDegree = () =>
    useForm<CreateDegreeFromLead>({
        resolver: zodResolver(PostDegreeSchema),
    });

export const useFormSubject = () =>
    useForm<CreateSubjectFromLead>({
        resolver: zodResolver(PostSubjectSchema),
    }); */