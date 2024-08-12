import { z } from "zod";
import { PostLeadSchema } from "../validation/LeadSchema";
import { useForm, useFormContext } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

export type Lead = z.infer<typeof PostLeadSchema>

export const useFormLead = () =>
    useForm<Lead>({
        resolver: zodResolver(PostLeadSchema),
    });

export const useFormContextLead = () =>
        useFormContext<Lead>()
