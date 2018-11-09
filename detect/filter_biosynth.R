#The R scritp reads the Blasttab_summary.tsv file from bgc_blast_tab.py
#and filters out those biosinthetic genes wich do not pass the stablished criteria
#The output BlastTab_summ.filtered.tsv follows the same format as the input

require(fitdistrplus)
require(ggplot2)
require(gridExtra)

args = commandArgs(trailingOnly=TRUE)
if (length(args)==0){
    stop("file name tsv and coverage length cutoff needed in arguments", call.=FALSE)
}
input=args[1]
coverage_cutoff=as.numeric(args[2])
poisson_cutoff=as.numeric(args[3])

dataBGC<-read.table(input, header = T , sep = "\t", stringsAsFactors = FALSE)
# calculate vector pecentage coverage
perc_cov<-dataBGC$coverage/dataBGC$subject_lenght

#cutoff coverave 100 aa for 75 bp reads, 200 aa  for 150 bp reads
#poisson distribution for paired reads
#cutoff=10 min number of paired hits, poisson: probaility of n events occurring
#in an interval with a rate= mean, and if events were independent of each other (they are not)

mean_percov<-mean(perc_cov)
mean_paired<-mean(dataBGC$paired_reads)
mean_hitnum<-mean(dataBGC$hit_number)

# P(X<x) under poisson asumption where lambda=mean_paired
# calculate quantile < 1e-6, minimun number of paired hits
cutoff_paired = qpois(poisson_cutoff, lambda = mean_paired)
cutoff_paired
#calculate p of selected quantile.
p_paired<-ppois(cutoff_paired, lambda = mean_paired, lower.tail=F)

# The higher the values of each gene, the more chance a a gene exist in the sample
# coding for similar (or the same) genes. Select those genes with higher values.

# recover BGC biosynthetic genes wich pass both cutoffs
dataBGC.filtered<-dataBGC[dataBGC$coverage>=coverage_cutoff & dataBGC$paired_reads>cutoff_paired,]
write.table(dataBGC.filtered, file = "BlastTab_summ.filtered.tsv",sep="\t", row.names=F, quote=F)

# plot genes wich surpassed the stablished filters
#figure color types
ptype <- rep(NA,length(x=length(dataBGC$coverage)))
ptype[dataBGC$paired_reads>cutoff_paired & dataBGC$coverage>=coverage_cutoff] <- "coverage and paired reads"
ptype[dataBGC$paired_reads>cutoff_paired & dataBGC$coverage<coverage_cutoff] <- "only paired reads"
tmp<-dataBGC$paired_reads<=cutoff_paired & dataBGC$coverage>=coverage_cutoff
ptype[tmp & dataBGC$subject_lenght< 170] <- "only coverage, s_length<170 aa"
ptype[tmp & dataBGC$subject_lenght>= 170] <- "only coverage, s_length>=170"
ptype <- factor(x=ptype)

#Figure 1
#plot subject coverage against Paired read hits.
#draw lines for cutoff values, coverage and number of paired reads
plot1<-qplot( dataBGC$coverage, dataBGC$paired_reads,color=ptype) + geom_point(size=1.5) +
  geom_hline(mapping=aes(yintercept=c(cutoff_paired)),color="red", lty=2) +
  geom_vline(mapping=aes(xintercept=c(coverage_cutoff)),color="red", lty=2)+
  xlab("Length coverage")+
  ylab("Number of paired hits")+ labs(color="type")

#Figure 2
#hit number against number of paired reads, previous color scheme    
plot2<-qplot( dataBGC$hit_number, dataBGC$paired_reads, color=ptype) + geom_point(size=2)+
  geom_hline(mapping=aes(yintercept=c(cutoff_paired)), color="red", lty=2) +
  labs(x="Number of hits" , y="Number of paired reads", color="type")

pdf("plot_pair_coverage.pdf")
grid.arrange(plot1, plot2)
dev.off()


