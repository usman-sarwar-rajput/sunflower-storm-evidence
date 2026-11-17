"""Offline sunflower evidence analysis. Run from anywhere with the bundled inputs."""
from pathlib import Path
import csv, hashlib, json
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
I, C, R, F = (ROOT/d for d in ('inputs','cleaned','results','figures'))
for d in (C,R,F): d.mkdir(exist_ok=True)
manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
for name, meta in manifest.items():
    assert hashlib.sha256((I/name).read_bytes()).hexdigest()==meta['sha256'], name

can=pd.read_csv(I/'Canopy Cover.csv',header=3,skiprows=[4],encoding='cp1252',na_values=['#NA'])
can['source_row']=can.index+6
can=can[['Year','Date','Plot','Tmnt','Blk','Canopy Cover','source_row']].rename(columns={'Plot':'plot','Tmnt':'treatment','Blk':'block','Canopy Cover':'cover_fraction'})
can['date']=pd.to_datetime(can.Date,format='%m/%d/%Y',errors='coerce')
can=can.dropna(subset=['date','cover_fraction']).drop(columns=['Date','Year']).sort_values(['date','plot'])
assert not can.duplicated(['date','plot']).any() and can.cover_fraction.between(0,1).all()
can['cover_percent']=can.cover_fraction*100
can.to_csv(C/'canopy_plot_observations.csv',index=False)
w=pd.read_csv(I/'LIRF Weather 2008-2016 Daily.csv',header=2,skiprows=[3,4],na_values=['#NA']).dropna(how='all')
w['date']=pd.to_datetime(w.Date,format='%m/%d/%Y')
assert len(w)==3288 and w.date.is_unique
w=w[['date','Precip','AirTemp_Max','DlySolRad','WindRun_Tot','Source','Notes']]
w.to_csv(C/'station_daily_weather.csv',index=False)
event=pd.Timestamp('2016-08-19')
early=pd.Timestamp('2016-07-17')
logs=pd.read_csv(I/'Crop Log.csv',header=3,encoding='cp1252')
assert logs.astype(str).apply(lambda c:c.str.contains('serious hail',case=False)).any().any()
assert 'August 19, 2016' in (I/'LIRF Sunflower Methodology.txt').read_text(encoding='cp1252')

same_year=can[can.date.dt.year.eq(2016)]
pivot=same_year.pivot(index='plot',columns='date',values='cover_percent')
b,a=pd.Timestamp('2016-08-18'),pd.Timestamp('2016-08-23')
pair=pivot[[b,a]].dropna().rename(columns={b:'before_percent',a:'after_percent'})
pair['change_percentage_points']=pair.after_percent-pair.before_percent
for date,label in [(b,'before'),(a,'after')]:
    pair=pair.join(same_year[same_year.date.eq(date)].set_index('plot').source_row.rename(label+'_source_row'),validate='one_to_one')
pair.to_csv(R/'hail_paired_plots.csv')
with (I/'Canopy Cover.csv').open(encoding='cp1252',newline='') as f: raw=list(csv.reader(f))
for plot,row in pair.iterrows():
    for label,date in [('before',b),('after',a)]:
        src=raw[int(row[label+'_source_row'])-1]
        assert src[3]==plot and pd.Timestamp(src[1])==date and abs(float(src[6])*100-row[label+'_percent'])<1e-9
assert len(pair)==48 and (pair.change_percentage_points<0).sum()==48
daily=same_year.groupby('date').cover_percent.agg(canopy_mean_percent='mean',canopy_sd_percent='std',plots='size').reset_index()
daily=daily.merge(w,on='date',how='left',validate='one_to_one')
daily.to_csv(R/'environment_matched_canopy_days.csv',index=False)

three=[('before',-3,-1),('hail_day',0,0),('after',1,3)]
five=[('earlier',-14,-8),('immediately_before',-7,-1),('hail_day',0,0),('immediately_after',1,7),('later',8,24)]
def phases(windows,name):
    parts=[]; summary=[]
    for phase,start,end in windows:
        low,high=event+pd.Timedelta(days=start),event+pd.Timedelta(days=end)
        x=w[w.date.between(low,high)].merge(daily[['date','canopy_mean_percent','plots']],on='date',how='left',validate='one_to_one')
        x.insert(0,'phase',phase); parts.append(x)
        summary.append(dict(phase=phase,start=low.date(),end=high.date(),calendar_days=len(x),canopy_days=int(x.plots.notna().sum()),canopy_plot_observations=int(x.plots.sum()),mean_canopy_percent=x.canopy_mean_percent.mean(),rain_mm=x.Precip.sum(min_count=len(x)),head_angle_observations=0))
    all_days=pd.concat(parts)
    assert all_days.date.is_unique
    all_days.to_csv(R/(name+'_daily.csv'),index=False)
    tab=pd.DataFrame(summary)
    tab.to_csv(R/(name+'_summary.csv'),index=False)
    return tab
short=phases(three,'three_period')
long=phases(five,'five_period')

# Context only: every consecutive observed 2016 canopy interval. One interval per pair of dates.
intervals=[]
for x,y in zip(pivot.columns[:-1],pivot.columns[1:]):
    q=pivot[[x,y]].dropna(); z=q[y]-q[x]
    intervals.append(dict(start=x.date(),end=y.date(),gap_days=(y-x).days,paired_plots=len(q),
                          mean_change_pp=z.mean(),decreased_plots=int((z<0).sum()),
                          includes_july_hail=x<=early<=y,includes_august_hail=x<=event<=y))
intervals=pd.DataFrame(intervals)
intervals.to_csv(R/'consecutive_canopy_intervals.csv',index=False)

# Published angle workbooks are deliberately independent from the event study.
head=pd.read_excel(I/'Head_Inclination.xlsx',sheet_name='headinclination_lm',dtype={'plot':str})
head.insert(0,'source_row',np.arange(2,len(head)+2))
assert len(head)==514 and head[['year_location','plot','trig_angle','lm_angle']].notna().all().all()
assert not head.duplicated(['year_location','plot']).any()
head['trig_minus_lm_deg']=head.trig_angle-head.lm_angle
head.to_csv(C/'head_inclination_method_comparison.csv',index=False)
angle=[]
for group,sub in list(head.groupby('year_location'))+[('all',head)]:
    delta=sub.trig_minus_lm_deg
    angle.append(dict(group=group,rows=len(sub),trig_mean_deg=sub.trig_angle.mean(),lm_mean_deg=sub.lm_angle.mean(),
                      mean_difference_deg=delta.mean(),mean_absolute_difference_deg=delta.abs().mean(),
                      rmse_difference_deg=np.sqrt((delta**2).mean()),sd_difference_deg=delta.std()))
angles=pd.DataFrame(angle)
angles.to_csv(R/'head_inclination_agreement.csv',index=False)
stem=pd.read_excel(I/'Brooks_2023_S13_Data.xlsx',sheet_name='Fig2B')
assert stem.shape==(64,7) and stem.time.tolist()==list(range(14,78)) and stem.notna().all().all()
st=stem.melt('time',var_name='plant_id',value_name='projected_stem_angle_deg').sort_values(['plant_id','time'])
st['absolute_hourly_change_deg']=st.groupby('plant_id').projected_stem_angle_deg.diff().abs()
st.to_csv(C/'juvenile_stem_angles.csv',index=False)
ranges=st.groupby('plant_id').projected_stem_angle_deg.agg(lambda a:a.max()-a.min())

def save(fig,name): fig.savefig(F/name,dpi=170,bbox_inches='tight'); plt.close(fig)
fig,ax=plt.subplots(2,1,figsize=(9,5),sharex=True,layout='constrained')
wx=w[w.date.between('2016-07-14','2016-09-12')]
ax[0].errorbar(daily.date,daily.canopy_mean_percent,yerr=daily.canopy_sd_percent,fmt='o-',capsize=2,color='#335f40',label='Plot mean ± SD')
ax[0].legend(frameon=False)
ax[0].set(ylabel='Green canopy (%)',title='Colorado sunflower plots around recorded hail')
ax[1].bar(wx.date,wx.Precip,color='#437693')
ax[1].set(ylabel='Rain (mm/day)',xlabel='Local calendar date in 2016')
for x in ax:
    for day in (early,event): x.axvline(day,ls='--',color='#a43d26')
    x.grid(axis='y',alpha=.2)
save(fig,'Canopy_and_weather.png')
fig,ax=plt.subplots(figsize=(9,3.4),layout='constrained')
means=long.mean_canopy_percent
ax.bar(long.phase,means.fillna(0),color='#427150')
for j,(n,v) in enumerate(zip(long.canopy_days,means)):
    ax.text(j, v+2 if n else 5, f'{v:.1f}% ({n} dates)' if n else 'No measurement',ha='center',fontsize=9)
ax.set(ylabel='Mean green canopy (%)',title='Five period view around 19 August 2016 hail',ylim=(0,100))
ax.set_xticks(range(5),['Earlier','Just before','Hail day','Just after','Later'])
save(fig,'Five_period_canopy.png')
fig,ax=plt.subplots(figsize=(8,4),layout='constrained')
for k,g in head.groupby('year_location'):
    ax.scatter((g.trig_angle+g.lm_angle)/2,g.trig_minus_lm_deg,s=12,alpha=.45,label=k)
ax.axhline(0,ls='--',color='#555')
ax.axhline(head.trig_minus_lm_deg.mean(),color='#335f40')
ax.set(xlabel='Average of two source angles (°)',ylabel='Trigonometric minus linear (°)',title='USDA head inclination methods compared on the same plot rows')
ax.legend(frameon=False)
save(fig,'Head_inclination_method_agreement.png')
fig,ax=plt.subplots(figsize=(8,3.5),layout='constrained')
for k,g in st.groupby('plant_id'): ax.plot(g.time,g.projected_stem_angle_deg,alpha=.6,label=k)
ax.set(xlabel='Workbook time (hours; no event clock)',ylabel='Projected stem angle (°)',title='Young sunflower stem movement baseline')
ax.legend(ncol=3,frameon=False)
save(fig,'Juvenile_stem_baseline.png')
metrics=dict(cover_records=len(can),weather_days=len(w),paired_plots=len(pair),before_mean_pct=pair.before_percent.mean(),
             after_mean_pct=pair.after_percent.mean(),paired_change_pp=pair.change_percentage_points.mean(),
             paired_decreased=int((pair.change_percentage_points<0).sum()),day_of_hail_rain_mm=float(w.loc[w.date.eq(event),'Precip'].iloc[0]),
             event_interval_change_rank_lowest=int((intervals.mean_change_pp< pair.change_percentage_points.mean()-1e-9).sum()+1),
             season_consecutive_intervals=len(intervals),head_rows=len(head),head_mean_abs_difference_deg=angles.iloc[-1].mean_absolute_difference_deg,
             head_mean_difference_deg=angles.iloc[-1].mean_difference_deg,stem_observations=len(st),stem_mean_range_deg=ranges.mean(),
             stem_median_hourly_change_deg=st.absolute_hourly_change_deg.median(),
             storm_matched_head_observations=0,forecast_status='not estimable',
             validation=['Input hashes matched','Unique canopy date and plot keys','Unique weather dates','Both phase sets have disjoint dates','All 96 paired canopy values and dates checked against workbook CSV source rows','Stem timeline and 514 inclination records checked'])
(R/'validation_and_findings.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
print(json.dumps(metrics,indent=2))
