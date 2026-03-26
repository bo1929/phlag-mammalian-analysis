mkdir -p preds && ls pred*.txt | xargs -I{} bash -c "echo `echo {} | sed 's/pred-//' | sed 's/-eap.*\.txt//'` >  preds/{} && tail -2 {} | head -1 | tr ',' '\n' >> preds/{}"
ls *I*.txt | xargs -I{} bash -c "echo -n'' {} && sed -n '5p' {} | sed 's/# //'"  |sed 's/pred\-//' | sed 's/\.txt/    /' | sed 's/\-eap.* /	/' > distances_chr$1.txt
sed -i 's/pred-//; s/\-eap.*\.txt//'  preds/*
paste preds/pred-*.txt > preds/preds-$2.txt

