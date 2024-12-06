

non_profile_service_choices = (
    ("aplicacion_pestañas", "Aplicación de pestañas"),
    ("desintoxicacion_ionica", "Desintoxicación iónica"),
    ("derpamen", "Derpamen"),
    ("diseño_cejas", "Diseño de cejas"),
    ("lifting_pestañas", "Lifting de pestañas"),
    ("limpieza_oidos", "Limpieza de oídos"),
    ("pedicure_spa", "Pedicure SPA"),
    ("facial", "Facial"),
    ("hollywood_pell", "Hollywood pell"),
    ("depilacion_laser", "Depilación laser"),
    ("masaje:drenaje", "Masaje: Drenaje linfático brasileño"),
    ("masaje:reductivo", "Masaje: Reductivo"),
    ("masaje:moldeador", "Masaje: Moldeador"),
    ("masaje:anticelulitis", "Masaje: Anti celulitis"),
    ("masaje:aparatologia", "Masaje: Aparatología")
)

with_profile_service_choices = (
    ("acido_hialuronico:labios", "Acido hialurónico - labios"),
    ("acido_hialuronico:nariz", "Acido hialurónico - nariz"),
    ("acido_hialuronico:menton", "Acido hialurónico - mentón"),
    ("toxina_botuliniea", "Toxina Botulíniea - Botox"),
    ("fibroblast:eliminacion_verrugas", "Fibroblast: Eliminación de verrugas"),
    ("fibroblast:eliminacion_tatuajes", "Fibroblast: Eliminación de tatuajes")
)

services = {
    "Sin consentimiento": {
        "aplicacion_pestañas": "Aplicación de pestañas"
    },
    "with_consent": {
        "acido_hialuronico:labios": "Acido hialurónico - labios"
    }
}

services2 = [
    (
        "Sin consentimiento", non_profile_service_choices,

    ),
    (
        "Con consentimiento", with_profile_service_choices
    )
]