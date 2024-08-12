import { useFieldArray } from "react-hook-form";
import { useFormContextLead } from "../hooks/FormHooks";



export const SubjectForm = ({ degreeIndex }: { degreeIndex: number }) => {
    const {
        register,
        control,
        formState: { errors },
    } = useFormContextLead();

    const { append, remove, fields } = useFieldArray({
        name: `degrees.${degreeIndex}.subjects`,
        control,
    })

    return (
        <div className='my-2'>
            {fields.map((subject, subjectIndex) => {
                return (
                    <div key={subject.id || subjectIndex} className='py-4'>
                        <div>
                            <div className='flex-between'>
                                <h5 className='mb-2'>Materia {subjectIndex + 1} </h5>
                                <button
                                    type='button'
                                    onClick={() => {
                                        remove(subjectIndex);
                                    }}
                                    className="btn btn-secondary"
                                >
                                    Remover materia
                                </button>
                            </div>
                            <label className="form-label mt-2">Nombre de la materia </label>
                            <input
                                className={`form-control ${errors.degrees?.[degreeIndex]?.subjects?.[subjectIndex]?.name ? 'is-invalid' : ''}`}
                                {...register(`degrees.${degreeIndex}.subjects.${subjectIndex}.name`)}
                            />
                            <div className='invalid-feedback'>
                                {errors.degrees?.[degreeIndex]?.subjects?.[subjectIndex]?.name?.message}
                            </div>
                            <label className="form-label mt-2">Duración en meses </label>
                            <input
                                type='number'
                                className={`form-control ${errors.degrees?.[degreeIndex]?.subjects?.[subjectIndex]?.duration_in_months ? 'is-invalid' : ''}`}
                                {...register(`degrees.${degreeIndex}.subjects.${subjectIndex}.duration_in_months`)}
                            />
                            <div className='invalid-feedback'>
                                {errors.degrees?.[degreeIndex]?.subjects?.[subjectIndex]?.duration_in_months?.message}
                            </div>
                            <label className="form-label mt-2">Año de inscripción </label>
                            <input
                                type='number'
                                className={`form-control ${errors.degrees?.[degreeIndex]?.subjects?.[subjectIndex]?.register_year ? 'is-invalid' : ''}`}
                                {...register(`degrees.${degreeIndex}.subjects.${subjectIndex}.register_year`)}
                            />
                            <div className='invalid-feedback'>
                                {errors.degrees?.[degreeIndex]?.subjects?.[subjectIndex]?.register_year?.message}
                            </div>
                            <label className="form-label mt-2">Número de veces cursada </label>
                            <input
                                type='number'
                                className={`form-control ${errors.degrees?.[degreeIndex]?.subjects?.[subjectIndex]?.times_taken ? 'is-invalid' : ''}`}
                                {...register(`degrees.${degreeIndex}.subjects.${subjectIndex}.times_taken`)}
                            />
                            <div className='invalid-feedback'>
                                {errors.degrees?.[degreeIndex]?.subjects?.[subjectIndex]?.times_taken?.message}
                            </div>
                        </div>
                    </div>
                );
            })}

            <button
                type='button'
                onClick={() => {
                    append({ name: '', duration_in_months: undefined, register_year: undefined, times_taken: undefined });
                }}
                className='btn btn-success'
            >
                Agregar materia
            </button>
            <hr />
        </div>
    );
};