"""Statistical add-on: hypothesis tests on D1 (Eurostat), D2 (bank annual reports), D3 (job ads), D4 (published surveys)."""
import pandas as pd, numpy as np, os
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.contingency_tables import mcnemar
import statsmodels.api as sm
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

R=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D=f'{R}/data'; O=f'{R}/out'; os.makedirs(O,exist_ok=True)
rows=[]; out=[]
def rec(h,data,test,stat,p,effect,n,note=''):
    rows.append(dict(hypothesis=h,data=data,test=test,statistic=round(stat,3),p_value=p,effect=effect,n=n,note=note))
def md(df): return df.to_markdown(index=False)

# ---------- D1 ----------
e=pd.read_csv(f'{D}/D1_eurostat.csv'); c=e[e.is_aggregate==0]
w=c.pivot(index='geo',columns='year')
out.append('## D1 Eurostat: descriptives (EU27 countries, % of enterprises / % of employment)\n')
out.append(md(c.groupby('year')[['ai_ge10','ai_ge250','ict_spec_pc_emp']].agg(['mean','median','std']).round(2).reset_index()))
for col,lab in [('ai_ge10','enterprises 10+ staff'),('ai_ge250','enterprises 250+ staff')]:
    for a,b in [(2023,2025),(2021,2025)]:
        x=w[(col,a)];y=w[(col,b)];d=y-x
        t=stats.ttest_rel(y,x,alternative='greater'); wx=stats.wilcoxon(y,x,alternative='greater')
        dz=d.mean()/d.std(ddof=1)
        rec(f'H5a: AI adoption rose {a}->{b} ({lab})','D1','Paired t-test (one-sided)',t.statistic,t.pvalue,f'mean diff {d.mean():.2f} pp; Cohen dz {dz:.2f}',len(d))
        rec(f'H5a: AI adoption rose {a}->{b} ({lab})','D1','Wilcoxon signed-rank (one-sided)',wx.statistic,wx.pvalue,f'median diff {d.median():.2f} pp; {int((d>0).sum())}/{len(d)} countries up',len(d))
fr=stats.friedmanchisquare(*[w[('ai_ge250',y)] for y in [2021,2023,2024,2025]])
rec('H5a: AI adoption differs across 2021/23/24/25 (250+)','D1','Friedman test',fr.statistic,fr.pvalue,'',len(w))
yr=2025; x=w[('ict_spec_pc_emp',yr)]; 
for col,lab in [('ai_ge10','10+'),('ai_ge250','250+')]:
    y=w[(col,yr)]; pr=stats.pearsonr(x,y); sr=stats.spearmanr(x,y)
    rec(f'H5b: ICT-specialist share correlates with AI adoption ({lab}, {yr})','D1','Pearson r',pr.statistic,pr.pvalue,f'r={pr.statistic:.2f}',len(x))
    rec(f'H5b: ICT-specialist share correlates with AI adoption ({lab}, {yr})','D1','Spearman rho',sr.statistic,sr.pvalue,f'rho={sr.statistic:.2f}',len(x))
ols=sm.OLS(w[('ai_ge10',yr)],sm.add_constant(x)).fit()
rec(f'H5b: OLS AI adoption(10+) = a + b*ICT share ({yr})','D1','Simple linear regression',ols.tvalues.iloc[1],ols.pvalues.iloc[1],f'b={ols.params.iloc[1]:.2f} pp per 1 pp ICT share; R2={ols.rsquared:.2f}',int(ols.nobs))
fig,ax=plt.subplots(1,2,figsize=(11,4))
c.groupby('year')[['ai_ge10','ai_ge250']].mean().plot(marker='o',ax=ax[0]); ax[0].set_title('Mean AI adoption, EU27 countries (%)'); ax[0].legend(['10+ staff','250+ staff']); ax[0].set_xticks(sorted(c.year.unique())); ax[0].set_xlabel('Year')
ax[1].scatter(x,w[('ai_ge10',yr)]); ax[1].plot(x,ols.predict(sm.add_constant(x)),'r-'); ax[1].set_xlabel('ICT specialists, % of employment'); ax[1].set_ylabel('AI adoption % (10+ staff)'); ax[1].set_title(f'ICT skills vs AI adoption, {yr}')
plt.tight_layout(); plt.savefig(f'{O}/fig_D1.png',dpi=150); plt.close()

# ---------- D2 ----------
b=pd.read_csv(f'{D}/D2_bank_reports.csv'); b=b[b.total_words.fillna(0)>0].copy()
dens=['ai_d','reskill_d','aigov_d','reg_d']; lab2={'ai_d':'AI','reskill_d':'reskilling','aigov_d':'AI governance','reg_d':'AI/digital regulation'}
pw=b.pivot(index='bank_code',columns='fy',values=dens+['aigov_body']).dropna()
pb=b[b.bank_code.isin(pw.index)]
out.append(f'\n## D2 Bank annual reports: term density per 10,000 words (banks coded in both FY2022 and FY2025, n={len(pw)})\n')
g=pb.groupby('fy')[dens].agg(['mean','median','std']).round(3); g.columns=[f'{a}_{b2}' for a,b2 in g.columns]
g['aigov_body_share']=pb.groupby('fy').aigov_body.mean().round(3); g['n']=pb.groupby('fy').size(); out.append(md(g.reset_index()))
f25=b[b.fy==2025]; g2=f25.groupby('region')[dens].median().round(3); g2['n']=f25.groupby('region').size()
out.append(f'\nFY2025 medians by region (all coded FY2025 reports, n={len(f25)}):\n'); out.append(md(g2.reset_index()))
for v in dens:
    x=pw[(v,2022)]; y=pw[(v,2025)]; d=y-x; h=f'H10a: {lab2[v]} term density rose FY2022->FY2025'
    t=stats.ttest_rel(y,x,alternative='greater'); dz=d.mean()/d.std(ddof=1)
    rec(h,'D2','Paired t-test (one-sided)',t.statistic,t.pvalue,f'mean diff {d.mean():.3f} per 10k words; Cohen dz {dz:.2f}',len(d))
    if (d!=0).any():
        wx=stats.wilcoxon(y,x,alternative='greater')
        rec(h,'D2','Wilcoxon signed-rank (one-sided)',wx.statistic,wx.pvalue,f'median diff {d.median():.3f}; {int((d>0).sum())}/{len(d)} banks up',len(d))
ct=pd.crosstab(pw[('aigov_body',2022)].astype(int),pw[('aigov_body',2025)].astype(int)).reindex(index=[0,1],columns=[0,1],fill_value=0)
mc=mcnemar(ct.values,exact=True)
rec('H10b: share of banks disclosing a named AI governance body changed FY2022->FY2025','D2','McNemar exact (two-sided)',mc.statistic,mc.pvalue,f'{ct.loc[0,1]} banks 0->1, {ct.loc[1,0]} banks 1->0; share {ct.loc[1].sum()/len(pw):.0%} -> {ct[1].sum()/len(pw):.0%}',len(pw))
sr=stats.spearmanr(f25.ai_d,f25.reskill_d)
rec('H10c: AI density correlates with reskilling density (FY2025)','D2','Spearman rho (two-sided)',sr.statistic,sr.pvalue,f'rho={sr.statistic:.2f}',len(f25))
uk=f25[f25.region=='UK']; eu=f25[f25.region=='EU']; ps=[]; idx=[]
for v in dens:
    mw=stats.mannwhitneyu(uk[v],eu[v],alternative='two-sided'); r_rb=1-2*mw.statistic/(len(uk)*len(eu))
    rec(f'H10d: UK vs EU banks differ in {lab2[v]} density (FY2025)','D2','Mann-Whitney U (two-sided)',mw.statistic,mw.pvalue,f'median UK {uk[v].median():.3f} vs EU {eu[v].median():.3f}; rank-biserial r={-r_rb:.2f}',len(uk)+len(eu),f'n={len(uk)} UK vs {len(eu)} EU'); ps.append(mw.pvalue); idx.append(len(rows)-1)
for i,a in zip(idx,multipletests(ps,method='holm')[1]): rows[i]['note']+=f'; Holm-adjusted p={a:.4f}'
fig,ax=plt.subplots(1,4,figsize=(13,3.6))
for a,v in zip(ax,dens):
    for bk in pw.index: a.plot([2022,2025],[pw.loc[bk,(v,2022)],pw.loc[bk,(v,2025)]],color='grey',alpha=.4,lw=.8)
    a.plot([2022,2025],[pw[(v,2022)].median(),pw[(v,2025)].median()],color='#0072B2',marker='o',lw=2.5,label='median')
    a.set_xticks([2022,2025]); a.set_title(f'{lab2[v]} terms'); a.set_ylabel('mentions per 10k words')
ax[0].legend(); plt.suptitle(f'Bank annual reports FY2022 vs FY2025 (n={len(pw)} banks)'); plt.tight_layout(); plt.savefig(f'{O}/fig_D2.png',dpi=150); plt.close()

# ---------- D3 ----------
j=pd.read_csv(f'{D}/D3_job_ads.csv'); skills=['data','reg','cyber','automation','cert','governance']
j['AI_exposed']=j.ai_ml.map({1:'AI-exposed',0:'Not AI-exposed'})
out.append('\n## D3 Job adverts: skill prevalence by group (% of adverts)\n')
tab=(j.groupby('AI_exposed')[skills].mean()*100).round(1); tab['n']=j.groupby('AI_exposed').size(); out.append(md(tab.reset_index()))
tab2=(j.groupby('role_type')[skills+['ai_ml']].mean()*100).round(1); tab2['n']=j.groupby('role_type').size(); out.append('\nBy title-based role type:\n'); out.append(md(tab2.reset_index()))
ps=[];idx=[]
for s in skills:
    ct=pd.crosstab(j.ai_ml,j[s]).reindex(index=[0,1],columns=[0,1],fill_value=0)
    chi,p,dof,ex=stats.chi2_contingency(ct,correction=False)
    if (ex<5).any(): 
        orr,p=stats.fisher_exact(ct); test='Fisher exact'; stat=orr
    else: test='Chi-square (1 df)'; stat=chi
    a,b,cc,dd=ct.loc[0,0],ct.loc[0,1],ct.loc[1,0],ct.loc[1,1]; orr=(dd*a)/(cc*b) if cc*b else np.nan
    v=np.sqrt(stats.chi2_contingency(ct,correction=False)[0]/ct.values.sum())
    rec(f'H6: AI-exposed adverts differ in demand for {s} skills','D3',test,stat,p,f'OR={orr:.2f}; phi={v:.2f}',int(ct.values.sum())); ps.append(p); idx.append(len(rows)-1)
adj=multipletests(ps,method='holm')[1]
for i,a in zip(idx,adj): rows[i]['note']=f'Holm-adjusted p={a:.4f}'
for s in skills:
    ct=pd.crosstab(j.role_type,j[s]).reindex(index=['Traditional','AI'],columns=[0,1],fill_value=0); orr,p=stats.fisher_exact(ct)
    rec(f'H6 (robustness): AI-titled vs traditional adverts, {s}','D3','Fisher exact',orr,p,f'OR={orr:.2f}',int(ct.values.sum()),'AI-titled n small; indicative')
sal=j.dropna(subset=['salary_annual_mid'])
for g,lab in [('ai_ml','AI-exposed vs not'),('role_type','AI-titled vs traditional')]:
    vals=sal.groupby(g).salary_annual_mid
    a=sal[sal[g].isin([1,'AI'])].salary_annual_mid; b=sal[sal[g].isin([0,'Traditional'])].salary_annual_mid
    mw=stats.mannwhitneyu(a,b,alternative='greater'); t=stats.ttest_ind(a,b,equal_var=False,alternative='greater')
    prem=(a.median()/b.median()-1)*100
    rec(f'H7: {lab} adverts offer higher pay','D3','Mann-Whitney U (one-sided)',mw.statistic,mw.pvalue,f'median £{a.median():,.0f} vs £{b.median():,.0f} ({prem:+.0f}%)',len(a)+len(b),f'n={len(a)} vs {len(b)}')
    rec(f'H7: {lab} adverts offer higher pay','D3','Welch t-test (one-sided)',t.statistic,t.pvalue,f'mean £{a.mean():,.0f} vs £{b.mean():,.0f}',len(a)+len(b))
k=int(j.ai_ml.sum()); n=len(j); lo,hi=proportion_confint(k,n,method='wilson')
out.append(f'\nShare of financial-services GRC adverts mentioning AI/ML: {k/n:.1%} (95% Wilson CI {lo:.1%} to {hi:.1%}), n={n}.\n')
fig,ax=plt.subplots(figsize=(8,4)); (tab[skills].T).plot.bar(ax=ax); ax.set_ylabel('% of adverts'); ax.set_title('Skills requested: AI-exposed vs other GRC adverts'); plt.xticks(rotation=0); plt.tight_layout(); plt.savefig(f'{O}/fig_D3.png',dpi=150); plt.close()

# ---------- D4 ----------
s=pd.read_csv(f'{D}/D4_survey_props.csv')
out.append('\n## D4 Published survey proportions with 95% Wilson CIs\n')
s2=s.dropna(subset=['n_respondents']).copy(); s2['n']=s2.n_respondents.astype(int)
s2[['ci_low','ci_high']]=s2.apply(lambda r: pd.Series(proportion_confint(round(r.proportion*r.n),r.n,method='wilson')),axis=1)
out.append(md(s2[['source','year','proportion','n','ci_low','ci_high']].round(3)))
z,p=proportions_ztest([round(.75*118),round(.58*71)],[118,71],alternative='larger')
rec('H8: share of UK FS firms using AI rose 2022->2024','D4','Two-proportion z-test (one-sided)',z,p,'58% (n=71) -> 75% (n=118)',189,'Different firm samples each wave')
z,p=proportions_ztest(round(.57*118),118,value=.5,alternative='larger')
rec('H9: majority of firms see talent/skills as a large or medium AI constraint','D4','One-sample z-test vs 50%',z,p,'25%+32%=57%',118)
for lab,pp,nn in [('IIA: experienced auditors need more tech skills',.96,6506),('TR: professionals expect high/transformative AI impact',.80,2275)]:
    z,p=proportions_ztest(round(pp*nn),nn,value=.5,alternative='larger'); rec(f'H9: majority agree - {lab}','D4','One-sample z-test vs 50%',z,p,f'{pp:.0%}',nn)

res=pd.DataFrame(rows); res['p_value']=res.p_value.map(lambda v: f'{v:.4f}' if v>=1e-4 else '<0.0001'); res.to_csv(f'{O}/test_results.csv',index=False)
open(f'{O}/results.md','w').write('# Statistical results\n\n## Hypothesis tests\n\n'+md(res)+'\n\n'+'\n'.join(out))
print(md(res)); print('\n'.join(out))
