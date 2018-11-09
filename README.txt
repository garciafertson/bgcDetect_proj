Readme detectar BGC en lecturas pareadas de metagenomas
El archivo contiene: Pipeline de los scripts escritos para detectar BGC en los archivos fastq de lecturas pareadas comparando contra una base de datos de BGC de genomas completos. 
Scripts escritos y dependencias
CONSTRUIR BASE DE DATOS
DB de BGC GBK. La primera base de datos está en una carpeta que contiene todos los archivos GBK detectados por AntiSMASH en el conjunto inicial de genomas.
DB de Biosynthetic BGC GBK. Esta base de datos en un archivo fasta con la secuencia de todos los genes anotados como biosintéticos de la base de datos de arriba.
El script de Python “gbk2faaBiosynt_allBGC.py” recibe el path de la carpeta que contiene los archivos GBK con los BGC. Trata de leer los archivos con extensión GBK y extrae de cada archivo uno los genes con anotados como biosintéticos, luego imprime en un archivo multifasta la secuencia de cada gen biosintético con un header con el siguiente formato: >gbkfilename; ncbiprot_accesion; bgc_cluster_type; bgc_gene_type, >AM412059.2.cluster009.gbk;CCC64645.1;t1pks;t1pks.Disminuimos la redundancia de secuencias con CD-hit, y un punto de corte -c 1, para eliminar secuencias idénticas. Con el archivo faa creamos una base de datos para para realizar búsquedas con Diamond Blastx. 
DETECCIÓN DE BGC EN LECTURAS DE MUESTRAS METAGENOMICAS
Como paso adicional tenemos usar solo las lecturas que no pudieron ser ensambladas, para obtener las lecturas sin ensablar mapeamos las lecturas originales sobre los contigs ensamblados usando bowtie (o algún otro programa para alineamientos), el archivo de salida está en formato SAM. Con Samtools transformamos a formato BAM.  Luego con la herramienta bam2fastq y la opción --no-aligned, regresamos al formato fastq a partir del alineamiento BAM excluyendo las lecturas que sí pudieron ser alineadas.
Tomamos los archivos R1.fastq y R2.fastq y corremos Diamond Blastx contra la la base de datos de genes biosintéticos, pedimos solo el mejor hit y establecemos un punto de corte mínimo de 1e-6. El archivo de salida está en formato Blast Tab. **revisar parámetros que le estoy pidiendo a blastx, “--top 1 or 100, --query-cover 80, delete alingments with reapeated querys, only one query per alignment  --max_targ_seq 0 , and post process output to get only top hit from all detected hits, preserve blast tab format**
Con el script “bgc_blast_tab.py” realizmos un conteo del número de hits que tuvo cada gen en la base de datos. EL script lee los resultados de diamond blastx en formato blast tab (R1.fastq y R2.fastq), el numero inicial de lecturas, y el archivo fasta con la base de datos de genes biosintéticos. El archivo de salida se llama Blasttab_summary.tsv (tab separated value) y contiene la siguiente información:
subject_id, el mismo header de cada secuencia en la base de datos
subject_length, longitud de la secuencia en aminoaciodos
hit_number, numero de reads que tuvieron hit con el gen de la base de datos 
coverage, extension de aminoacidos cubiertos en la base de datos
paired_reads, numero de reads pareados con hit en el gen
bits, score de bits acumulados del total de hits en el gen
mean_e_value.  Valor promedio del e value del total de hits acumulados en el gen.
El script de R “detectBGCinSGreads.R” lee el archivo de salida anterior y de acuerdo con puntos de corte establecidos señala si un gen biosintético supera los puntos de corte establecidos.
**el siguiente paso es comparar ver la cobertura de genes biosintéticos, es decir, el numero de genes biosintéticos detectados respecto al total de genes biosintéticos en el GBK original**
**realizar un bash script para crear la base de datos (archivo fasta y base de datos dmnd) a partir de la carpeta con los archivos gbk. Enlistar dependencias y organizar custom scripts en carpetas para poder trasladar a otras máquinas. Requiere cd-hit, diamond-blastx, python 2.7 modulos biopython, seqio
gbk2faaBiosynt_allBGC.py --path /path/to/DB_folder/with_gbk_file --out BGCbiosynth.faa
cd-hit -c 1 -i BGCbiosynth.faa -o BGCcdhit100_biosynth.faa
diamond makedb –in BGCcdhit100_biosynth.faa –out BGCcdhit100_biosynth.faa.dmnd

**realizar bash script para deterctar bgc a partir de archivos R1fastq y R2fastq (con las lecturas que no pudieron ser esmbladas). Enlistar dependencias y organizar custom scripts necesarios. Requiere diamond blastx, Python 2.7 modulos bioython seqio.
diamond *-top 1 -e 1e-5 -db BGCcdhit100_biosynth.faa.dmnd -input R1.fastq -output R1fastq.tab
diamond *-top 1 -e 1e-5 -db BGCcdhit100_biosynth.faa.dmnd -input R2.fastq -output R2fastq.tab
#actualmente está corriendo Python con -max_target_seqs, modificar para regresar solo el mejor hit entre todos los posibles #falta ajustar el punto corte al tamaño de la lectura
bgc_blast_tab.py --blastR1 R1fastq.tab --blastR2 R2fastq.tab –blast_db BGCcdhit100_biosynth.faa --n-reads 100 #por el momento n-reads no se utiliza (archivo de salida Blasttab_summary.tsv )
detectBGCinSGreads.R Blasttab_summary.tsv 

Luego observmos la cobertura de genes biosintéticos, es decir, el número de genes biosintéticos detectados respecto al total de genes biosintéticos en el GBK original**
Este paso lo realiza un script de Python, el script recibe como entrada la base de datos de genes de genes biosintéticos de BGC BGCbiosynthcdhit100.faa y el archivo con la lista de genes que pasaron los puntos de corte: BLastTab_summ.filtered.tsv (número de hits pareados y cobertura sobre el gen biosinético). El script calcula para cada BGC en la base de datos el porcentaje de genes biosintéticos que pasaron el filtro respecto al total de genes biosintéticos en el BGC y ordena los BGC de mayor a menor cobertura. La salida reporta en líneas que comienzan con # el nombre del BGC y el porcentaje de cobertura de genes biosintéticos que tuvo, en líneas que empiezan con \t las estadísticas para cada gen biosintético detectado del BGC.

** el siguiente paso sería mapear los reads sobre el resto de los genes de los BGC detectados.

