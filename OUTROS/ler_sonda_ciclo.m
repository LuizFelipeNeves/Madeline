%exemplo de ciclo diário de radiação solar global (W m-2)
close all; clear all;clc


%diretório principal
dir='C:\Users\anthony\Desktop\sonda\';
%nome arquivo
nomeplan='BRB1511ED.txt';
%leitura arquivo
Xbase=load([dir nomeplan]);
%seleciona coluna dias
listadias=Xbase(:,3);
%seleciona primeiro dia disponível
diaini=listadias(1);
%seleciona último dia disponível
diafim=listadias($);
%gera vetor dia juliano para o mês específico
vetordias=diaini:1:diafim;
%calcula o número de dias entre diaini e diafim;
ndias=length(vetordias);
X=[];
%loop para cada dia
for i=1:ndias
   %seta o dia juliano 
   dj=vetordias(i);
   %encontra a posição das linhas correspondentes ao dia juliano (dj)
   inddia=find(listadias==dj);
   %cria matriz X baseando-se nas linhas do dj;
   X=Xbase(inddia,:);
   %seleciona no vetor X coluna minuto
   vetor_min=X(:,4);
   %seleciona no vetor X coluna irradiância
   G=X(:,5);
   
   %plotagem de figura para cada dia juliano
   %figura
   figure(1);clf
   plot(vetor_min,G,'-b'); hold on
%    grid on
   V=[0 1440 0 1400]; 
   axis(V);
   title([nomeplan '     DJ(atual)=' num2str(dj) ' DJ(final)=' num2str(diafim)]);
   xlabel('Minuto do dia');
   ylabel('Irradiância solar Wm^{-2}');
   %------------------------------------
   pause
   clear X
end


