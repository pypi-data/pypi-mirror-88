# A tool to convert DataFrame to a list of objects of some class or vice versa
  - Signatures
  ```python
    def df2obs(df: pd.DataFrame, clazz: Any) -> List[Any]
  ```
  or
  ```python
    def obs2df(obs: List[Any]) -> pd.DataFrame
  ```
# How to use
  - Define class attribute : pandas DataFrame column mapping in your class directly
  - Inherit your class from df2obs.base.Base, and make df2obs.base.BaseType as its metaclass
  - You are ready to go using df2obs() and/or obs2df()
# Example
  ```python
  import pandas as pd
  from df2obs.base import Base, BaseType


  movie_df = pd.DataFrame({
      'title1': ['The American President', "Queen's Gambit", 'Wall Street'],
      'year1': [1995, 2020, 1987],
      'director2': ['Rob Reiner', 'Scott Frank', 'Oliver Stone']
  })


  class Movie(Base, metaclass=BaseType):
      # class attribute = pandas DataFrame column name
      title = 'title1'
      year = 'year1'
      director = 'director2'


  if __name__ == "__main__":
      m = Movie()
      packed_obs = list(m.df2obs(movie_df))
      print(packed_obs)
      print('='*100)
      print(m.obs2df(packed_obs))
  ```

  ```markdown
  Result:

  [{'title': 'The American President', 'year': 1995, 'director': 'Rob Reiner'}, {'title': "Queen's Gambit", 'year': 2020, 'director': 'Scott Frank'}, {'title': 'Wall  Street', 'year': 1987, 'director': 'Oliver Stone'}]
  ====================================================================================================
                    title  year      director
  0  The American President  1995    Rob Reiner
  1          Queen's Gambit  2020   Scott Frank
  2             Wall Street  1987  Oliver Stone
  ```