library(RODBC)
library(ggplot2)
library(dplyr)


args <- commandArgs(trailingOnly = TRUE)
# The first argument is the database path (whatever Python passed)
db_path <- args[1]

channel <- odbcConnectAccess2007(db_path)

otolith <- sqlQuery(channel,"select * from Otolith ORDER BY Otolith_number")

figure <- ggplot() +
  geom_point(data=otolith, aes(x=Length, y=Weight),size=0.4) +
  geom_point(data=otolith[nrow(otolith),], aes(x=Length, y=Weight), size=0.8, color="Red") +
  theme_classic() +
  theme(axis.text = element_text(size=4),
        axis.title = element_blank(),
        plot.margin = unit(c(0.1, 0.1, 0.1, 0.1), "cm")) 


script_dir <- dirname(dirname(db_path))  # Go up from db to project root
plot_path <- file.path(script_dir, "SableSpecimen","Otolith_Entry", "lw_plot.png")


ggsave(filename=plot_path, plot=figure, height=280, width=360, units=c("px"))
