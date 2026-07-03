# IA generativa para imágenes — material de la charla

Slides en LaTeX Beamer sobre IA generativa aplicada a imágenes: qué es, sus
antecedentes, herramientas, casos especiales y errores/riesgos comunes.

```
IA_generativa_beamer/
├── IA_generativa_imagenes.tex   # Fuente de la presentación
└── final_images/                 # Imágenes usadas en las slides
```

## Compilar

```bash
pdflatex IA_generativa_imagenes.tex
pdflatex IA_generativa_imagenes.tex
```

Genera `IA_generativa_imagenes.pdf`. Requiere una instalación de TeX Live con
`beamer` (usa el tema `Madrid`) y las imágenes de `final_images/` en la misma
carpeta relativa.

## Contenido

1. ¿Se puede crear con la IA?
2. IA Generativa
3. IA generativa en imágenes (Antecedentes)
4. Herramientas
5. Casos especiales
6. Errores, ataques y desempeño
7. Conclusiones
