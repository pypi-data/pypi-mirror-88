// A Bison parser, made by GNU Bison 3.7.3.

// Skeleton implementation for Bison LALR(1) parsers in C++

// Copyright (C) 2002-2015, 2018-2020 Free Software Foundation, Inc.

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

// As a special exception, you may create a larger work that contains
// part or all of the Bison parser skeleton and distribute that work
// under terms of your choice, so long as that work isn't itself a
// parser generator using the skeleton or a modified version thereof
// as a parser skeleton.  Alternatively, if you modify or redistribute
// the parser skeleton itself, you may (at your option) remove this
// special exception, which will cause the skeleton and the resulting
// Bison output files to be licensed under the GNU General Public
// License without this special exception.

// This special exception was added by the Free Software Foundation in
// version 2.2 of Bison.

// DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
// especially those whose name start with YY_ or yy_.  They are
// private implementation details that can be changed or removed.


// Take the name prefix into account.
#define yylex   pytypelex



#include "parser.tab.hh"


// Unqualified %code blocks.
#line 34 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"

namespace {
PyObject* DOT_STRING = PyString_FromString(".");

/* Helper functions for building up lists. */
PyObject* StartList(PyObject* item);
PyObject* AppendList(PyObject* list, PyObject* item);
PyObject* ExtendList(PyObject* dst, PyObject* src);

}  // end namespace


// Check that a python value is not NULL.  This must be a macro because it
// calls YYERROR (which is a goto).
#define CHECK(x, loc) do { if (x == NULL) {\
    ctx->SetErrorLocation(loc); \
    YYERROR; \
  }} while(0)

// pytypelex is generated in lexer.lex.cc, but because it uses semantic_type and
// location, it must be declared here.
int pytypelex(pytype::parser::semantic_type* lvalp, pytype::location* llocp,
              void* scanner);


#line 74 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"


#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> // FIXME: INFRINGES ON USER NAME SPACE.
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif


// Whether we are compiled with exception support.
#ifndef YY_EXCEPTIONS
# if defined __GNUC__ && !defined __EXCEPTIONS
#  define YY_EXCEPTIONS 0
# else
#  define YY_EXCEPTIONS 1
# endif
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K].location)
/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

# ifndef YYLLOC_DEFAULT
#  define YYLLOC_DEFAULT(Current, Rhs, N)                               \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).begin  = YYRHSLOC (Rhs, 1).begin;                   \
          (Current).end    = YYRHSLOC (Rhs, N).end;                     \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).begin = (Current).end = YYRHSLOC (Rhs, 0).end;      \
        }                                                               \
    while (false)
# endif


// Enable debugging if requested.
#if PYTYPEDEBUG

// A pseudo ostream that takes yydebug_ into account.
# define YYCDEBUG if (yydebug_) (*yycdebug_)

# define YY_SYMBOL_PRINT(Title, Symbol)         \
  do {                                          \
    if (yydebug_)                               \
    {                                           \
      *yycdebug_ << Title << ' ';               \
      yy_print_ (*yycdebug_, Symbol);           \
      *yycdebug_ << '\n';                       \
    }                                           \
  } while (false)

# define YY_REDUCE_PRINT(Rule)          \
  do {                                  \
    if (yydebug_)                       \
      yy_reduce_print_ (Rule);          \
  } while (false)

# define YY_STACK_PRINT()               \
  do {                                  \
    if (yydebug_)                       \
      yy_stack_print_ ();                \
  } while (false)

#else // !PYTYPEDEBUG

# define YYCDEBUG if (false) std::cerr
# define YY_SYMBOL_PRINT(Title, Symbol)  YYUSE (Symbol)
# define YY_REDUCE_PRINT(Rule)           static_cast<void> (0)
# define YY_STACK_PRINT()                static_cast<void> (0)

#endif // !PYTYPEDEBUG

#define yyerrok         (yyerrstatus_ = 0)
#define yyclearin       (yyla.clear ())

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYRECOVERING()  (!!yyerrstatus_)

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
namespace pytype {
#line 167 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

  /// Build a parser object.
  parser::parser (void* scanner_yyarg, pytype::Context* ctx_yyarg)
#if PYTYPEDEBUG
    : yydebug_ (false),
      yycdebug_ (&std::cerr),
#else
    :
#endif
      scanner (scanner_yyarg),
      ctx (ctx_yyarg)
  {}

  parser::~parser ()
  {}

  parser::syntax_error::~syntax_error () YY_NOEXCEPT YY_NOTHROW
  {}

  /*---------------.
  | symbol kinds.  |
  `---------------*/

  // basic_symbol.
  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (const basic_symbol& that)
    : Base (that)
    , value (that.value)
    , location (that.location)
  {}


  /// Constructor for valueless symbols.
  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, YY_MOVE_REF (location_type) l)
    : Base (t)
    , value ()
    , location (l)
  {}

  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, YY_RVREF (semantic_type) v, YY_RVREF (location_type) l)
    : Base (t)
    , value (YY_MOVE (v))
    , location (YY_MOVE (l))
  {}

  template <typename Base>
  parser::symbol_kind_type
  parser::basic_symbol<Base>::type_get () const YY_NOEXCEPT
  {
    return this->kind ();
  }

  template <typename Base>
  bool
  parser::basic_symbol<Base>::empty () const YY_NOEXCEPT
  {
    return this->kind () == symbol_kind::S_YYEMPTY;
  }

  template <typename Base>
  void
  parser::basic_symbol<Base>::move (basic_symbol& s)
  {
    super_type::move (s);
    value = YY_MOVE (s.value);
    location = YY_MOVE (s.location);
  }

  // by_kind.
  parser::by_kind::by_kind ()
    : kind_ (symbol_kind::S_YYEMPTY)
  {}

#if 201103L <= YY_CPLUSPLUS
  parser::by_kind::by_kind (by_kind&& that)
    : kind_ (that.kind_)
  {
    that.clear ();
  }
#endif

  parser::by_kind::by_kind (const by_kind& that)
    : kind_ (that.kind_)
  {}

  parser::by_kind::by_kind (token_kind_type t)
    : kind_ (yytranslate_ (t))
  {}

  void
  parser::by_kind::clear ()
  {
    kind_ = symbol_kind::S_YYEMPTY;
  }

  void
  parser::by_kind::move (by_kind& that)
  {
    kind_ = that.kind_;
    that.clear ();
  }

  parser::symbol_kind_type
  parser::by_kind::kind () const YY_NOEXCEPT
  {
    return kind_;
  }

  parser::symbol_kind_type
  parser::by_kind::type_get () const YY_NOEXCEPT
  {
    return this->kind ();
  }


  // by_state.
  parser::by_state::by_state () YY_NOEXCEPT
    : state (empty_state)
  {}

  parser::by_state::by_state (const by_state& that) YY_NOEXCEPT
    : state (that.state)
  {}

  void
  parser::by_state::clear () YY_NOEXCEPT
  {
    state = empty_state;
  }

  void
  parser::by_state::move (by_state& that)
  {
    state = that.state;
    that.clear ();
  }

  parser::by_state::by_state (state_type s) YY_NOEXCEPT
    : state (s)
  {}

  parser::symbol_kind_type
  parser::by_state::kind () const YY_NOEXCEPT
  {
    if (state == empty_state)
      return symbol_kind::S_YYEMPTY;
    else
      return YY_CAST (symbol_kind_type, yystos_[+state]);
  }

  parser::stack_symbol_type::stack_symbol_type ()
  {}

  parser::stack_symbol_type::stack_symbol_type (YY_RVREF (stack_symbol_type) that)
    : super_type (YY_MOVE (that.state), YY_MOVE (that.value), YY_MOVE (that.location))
  {
#if 201103L <= YY_CPLUSPLUS
    // that is emptied.
    that.state = empty_state;
#endif
  }

  parser::stack_symbol_type::stack_symbol_type (state_type s, YY_MOVE_REF (symbol_type) that)
    : super_type (s, YY_MOVE (that.value), YY_MOVE (that.location))
  {
    // that is emptied.
    that.kind_ = symbol_kind::S_YYEMPTY;
  }

#if YY_CPLUSPLUS < 201103L
  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (const stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    return *this;
  }

  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    // that is emptied.
    that.state = empty_state;
    return *this;
  }
#endif

  template <typename Base>
  void
  parser::yy_destroy_ (const char* yymsg, basic_symbol<Base>& yysym) const
  {
    if (yymsg)
      YY_SYMBOL_PRINT (yymsg, yysym);

    // User destructor.
    switch (yysym.kind ())
    {
      case symbol_kind::S_NAME: // NAME
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 374 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_NUMBER: // NUMBER
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 380 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_STRING: // STRING
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 386 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_LEXERROR: // LEXERROR
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 392 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_start: // start
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 398 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_unit: // unit
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 404 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_alldefs: // alldefs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 410 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_classdef: // classdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 416 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_class_name: // class_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 422 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_parents: // parents
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 428 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_parent_list: // parent_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 434 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_parent: // parent
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 440 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_class_funcs: // maybe_class_funcs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 446 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_class_funcs: // class_funcs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 452 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_funcdefs: // funcdefs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 458 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_if_stmt: // if_stmt
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 464 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_if_and_elifs: // if_and_elifs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 470 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_class_if_stmt: // class_if_stmt
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 476 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_class_if_and_elifs: // class_if_and_elifs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 482 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_if_cond: // if_cond
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 488 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_elif_cond: // elif_cond
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 494 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_else_cond: // else_cond
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 500 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_condition: // condition
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 506 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_version_tuple: // version_tuple
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 512 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_condition_op: // condition_op
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.str)); }
#line 518 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_constantdef: // constantdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 524 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_importdef: // importdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 530 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_import_items: // import_items
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 536 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_import_item: // import_item
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 542 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_import_name: // import_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 548 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_from_list: // from_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 554 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_from_items: // from_items
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 560 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_from_item: // from_item
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 566 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_alias_or_constant: // alias_or_constant
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 572 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_string_list: // maybe_string_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 578 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_string_list: // string_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 584 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typevardef: // typevardef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 590 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typevar_args: // typevar_args
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 596 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typevar_kwargs: // typevar_kwargs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 602 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typevar_kwarg: // typevar_kwarg
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 608 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_funcdef: // funcdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 614 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_funcname: // funcname
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 620 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_decorators: // decorators
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 626 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_decorator: // decorator
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 632 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_async: // maybe_async
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 638 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_params: // params
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 644 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_param_list: // param_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 650 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_param: // param
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 656 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_param_type: // param_type
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 662 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_param_default: // param_default
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 668 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_param_star_name: // param_star_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 674 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_return: // return
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 680 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_body: // maybe_body
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 686 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_body: // body
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 692 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_body_stmt: // body_stmt
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 698 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type_parameters: // type_parameters
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 704 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type_parameter: // type_parameter
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 710 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_type_list: // maybe_type_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 716 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type_list: // type_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 722 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type: // type
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 728 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_named_tuple_fields: // named_tuple_fields
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 734 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_named_tuple_field_list: // named_tuple_field_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 740 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_named_tuple_field: // named_tuple_field
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 746 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_coll_named_tuple_fields: // coll_named_tuple_fields
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 752 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_coll_named_tuple_field_list: // coll_named_tuple_field_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 758 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_coll_named_tuple_field: // coll_named_tuple_field
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 764 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typed_dict_fields: // typed_dict_fields
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 770 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typed_dict_field_dict: // typed_dict_field_dict
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 776 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typed_dict_field: // typed_dict_field
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 782 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_typed_dict_kwarg: // maybe_typed_dict_kwarg
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 788 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type_tuple_elements: // type_tuple_elements
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 794 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type_tuple_literal: // type_tuple_literal
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 800 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_dotted_name: // dotted_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 806 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_getitem_key: // getitem_key
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 812 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_number: // maybe_number
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 818 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      default:
        break;
    }
  }

#if PYTYPEDEBUG
  template <typename Base>
  void
  parser::yy_print_ (std::ostream& yyo, const basic_symbol<Base>& yysym) const
  {
    std::ostream& yyoutput = yyo;
    YYUSE (yyoutput);
    if (yysym.empty ())
      yyo << "empty symbol";
    else
      {
        symbol_kind_type yykind = yysym.kind ();
        yyo << (yykind < YYNTOKENS ? "token" : "nterm")
            << ' ' << yysym.name () << " ("
            << yysym.location << ": ";
        YYUSE (yykind);
        yyo << ')';
      }
  }
#endif

  void
  parser::yypush_ (const char* m, YY_MOVE_REF (stack_symbol_type) sym)
  {
    if (m)
      YY_SYMBOL_PRINT (m, sym);
    yystack_.push (YY_MOVE (sym));
  }

  void
  parser::yypush_ (const char* m, state_type s, YY_MOVE_REF (symbol_type) sym)
  {
#if 201103L <= YY_CPLUSPLUS
    yypush_ (m, stack_symbol_type (s, std::move (sym)));
#else
    stack_symbol_type ss (s, sym);
    yypush_ (m, ss);
#endif
  }

  void
  parser::yypop_ (int n)
  {
    yystack_.pop (n);
  }

#if PYTYPEDEBUG
  std::ostream&
  parser::debug_stream () const
  {
    return *yycdebug_;
  }

  void
  parser::set_debug_stream (std::ostream& o)
  {
    yycdebug_ = &o;
  }


  parser::debug_level_type
  parser::debug_level () const
  {
    return yydebug_;
  }

  void
  parser::set_debug_level (debug_level_type l)
  {
    yydebug_ = l;
  }
#endif // PYTYPEDEBUG

  parser::state_type
  parser::yy_lr_goto_state_ (state_type yystate, int yysym)
  {
    int yyr = yypgoto_[yysym - YYNTOKENS] + yystate;
    if (0 <= yyr && yyr <= yylast_ && yycheck_[yyr] == yystate)
      return yytable_[yyr];
    else
      return yydefgoto_[yysym - YYNTOKENS];
  }

  bool
  parser::yy_pact_value_is_default_ (int yyvalue)
  {
    return yyvalue == yypact_ninf_;
  }

  bool
  parser::yy_table_value_is_error_ (int yyvalue)
  {
    return yyvalue == yytable_ninf_;
  }

  int
  parser::operator() ()
  {
    return parse ();
  }

  int
  parser::parse ()
  {
    int yyn;
    /// Length of the RHS of the rule being reduced.
    int yylen = 0;

    // Error handling.
    int yynerrs_ = 0;
    int yyerrstatus_ = 0;

    /// The lookahead symbol.
    symbol_type yyla;

    /// The locations where the error started and ended.
    stack_symbol_type yyerror_range[3];

    /// The return value of parse ().
    int yyresult;

#if YY_EXCEPTIONS
    try
#endif // YY_EXCEPTIONS
      {
    YYCDEBUG << "Starting parse\n";


    /* Initialize the stack.  The initial state will be set in
       yynewstate, since the latter expects the semantical and the
       location values to have been already stored, initialize these
       stacks with a primary value.  */
    yystack_.clear ();
    yypush_ (YY_NULLPTR, 0, YY_MOVE (yyla));

  /*-----------------------------------------------.
  | yynewstate -- push a new symbol on the stack.  |
  `-----------------------------------------------*/
  yynewstate:
    YYCDEBUG << "Entering state " << int (yystack_[0].state) << '\n';
    YY_STACK_PRINT ();

    // Accept?
    if (yystack_[0].state == yyfinal_)
      YYACCEPT;

    goto yybackup;


  /*-----------.
  | yybackup.  |
  `-----------*/
  yybackup:
    // Try to take a decision without lookahead.
    yyn = yypact_[+yystack_[0].state];
    if (yy_pact_value_is_default_ (yyn))
      goto yydefault;

    // Read a lookahead token.
    if (yyla.empty ())
      {
        YYCDEBUG << "Reading a token\n";
#if YY_EXCEPTIONS
        try
#endif // YY_EXCEPTIONS
          {
            yyla.kind_ = yytranslate_ (yylex (&yyla.value, &yyla.location, scanner));
          }
#if YY_EXCEPTIONS
        catch (const syntax_error& yyexc)
          {
            YYCDEBUG << "Caught exception: " << yyexc.what() << '\n';
            error (yyexc);
            goto yyerrlab1;
          }
#endif // YY_EXCEPTIONS
      }
    YY_SYMBOL_PRINT ("Next token is", yyla);

    if (yyla.kind () == symbol_kind::S_YYerror)
    {
      // The scanner already issued an error message, process directly
      // to error recovery.  But do not keep the error token as
      // lookahead, it is too special and may lead us to an endless
      // loop in error recovery. */
      yyla.kind_ = symbol_kind::S_YYUNDEF;
      goto yyerrlab1;
    }

    /* If the proper action on seeing token YYLA.TYPE is to reduce or
       to detect an error, take that action.  */
    yyn += yyla.kind ();
    if (yyn < 0 || yylast_ < yyn || yycheck_[yyn] != yyla.kind ())
      {
        goto yydefault;
      }

    // Reduce or error.
    yyn = yytable_[yyn];
    if (yyn <= 0)
      {
        if (yy_table_value_is_error_ (yyn))
          goto yyerrlab;
        yyn = -yyn;
        goto yyreduce;
      }

    // Count tokens shifted since error; after three, turn off error status.
    if (yyerrstatus_)
      --yyerrstatus_;

    // Shift the lookahead token.
    yypush_ ("Shifting", state_type (yyn), YY_MOVE (yyla));
    goto yynewstate;


  /*-----------------------------------------------------------.
  | yydefault -- do the default action for the current state.  |
  `-----------------------------------------------------------*/
  yydefault:
    yyn = yydefact_[+yystack_[0].state];
    if (yyn == 0)
      goto yyerrlab;
    goto yyreduce;


  /*-----------------------------.
  | yyreduce -- do a reduction.  |
  `-----------------------------*/
  yyreduce:
    yylen = yyr2_[yyn];
    {
      stack_symbol_type yylhs;
      yylhs.state = yy_lr_goto_state_ (yystack_[yylen].state, yyr1_[yyn]);
      /* If YYLEN is nonzero, implement the default value of the
         action: '$$ = $1'.  Otherwise, use the top of the stack.

         Otherwise, the following line sets YYLHS.VALUE to garbage.
         This behavior is undocumented and Bison users should not rely
         upon it.  */
      if (yylen)
        yylhs.value = yystack_[yylen - 1].value;
      else
        yylhs.value = yystack_[0].value;

      // Default location.
      {
        stack_type::slice range (yystack_, yylen);
        YYLLOC_DEFAULT (yylhs.location, range, yylen);
        yyerror_range[1].location = yylhs.location;
      }

      // Perform the reduction.
      YY_REDUCE_PRINT (yyn);
#if YY_EXCEPTIONS
      try
#endif // YY_EXCEPTIONS
        {
          switch (yyn)
            {
  case 2: // start: unit "end of file"
#line 135 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1089 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 3: // start: TRIPLEQUOTED unit "end of file"
#line 136 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                          { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1095 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 4: // unit: alldefs
#line 140 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1101 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 5: // alldefs: alldefs constantdef
#line 144 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                        { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1107 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 6: // alldefs: alldefs funcdef
#line 145 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1113 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 7: // alldefs: alldefs importdef
#line 146 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1119 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 8: // alldefs: alldefs alias_or_constant
#line 147 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                              {
      (yylhs.value.obj) = (yystack_[1].value.obj);
      PyObject* tmp = ctx->Call(kAddAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
    }
#line 1130 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 9: // alldefs: alldefs classdef
#line 153 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1136 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 10: // alldefs: alldefs typevardef
#line 154 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1142 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 11: // alldefs: alldefs if_stmt
#line 155 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1152 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 12: // alldefs: %empty
#line 160 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 1158 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 15: // classdef: decorators CLASS class_name parents ':' maybe_type_ignore maybe_class_funcs
#line 173 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewClass, "(NNNN)", (yystack_[6].value.obj), (yystack_[4].value.obj), (yystack_[3].value.obj), (yystack_[0].value.obj));
      // Fix location tracking. See funcdef.
      yylhs.location.begin = yystack_[4].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1169 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 16: // class_name: NAME
#line 182 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         {
      // Do not borrow the $1 reference since it is also returned later
      // in $$.  Use O instead of N in the format string.
      PyObject* tmp = ctx->Call(kRegisterClassName, "(O)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
      (yylhs.value.obj) = (yystack_[0].value.obj);
    }
#line 1182 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 17: // parents: '(' parent_list ')'
#line 193 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                        { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1188 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 18: // parents: '(' ')'
#line 194 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyList_New(0); }
#line 1194 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 19: // parents: %empty
#line 195 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = PyList_New(0); }
#line 1200 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 20: // parent_list: parent_list ',' parent
#line 199 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1206 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 21: // parent_list: parent
#line 200 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1212 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 22: // parent: type
#line 204 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1218 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 23: // parent: NAME '=' type
#line 205 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1224 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 24: // parent: NAMEDTUPLE
#line 206 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = PyString_FromString("NamedTuple"); }
#line 1230 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 25: // parent: TYPEDDICT
#line 207 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              {
      (yylhs.value.obj) = ctx->Call(kNewType, "(N)", PyString_FromString("TypedDict"));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1239 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 26: // maybe_class_funcs: pass_or_ellipsis maybe_type_ignore
#line 214 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       { (yylhs.value.obj) = PyList_New(0); }
#line 1245 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 27: // maybe_class_funcs: INDENT class_funcs DEDENT
#line 215 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                              { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1251 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 28: // maybe_class_funcs: INDENT TRIPLEQUOTED class_funcs DEDENT
#line 216 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                           { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1257 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 29: // class_funcs: pass_or_ellipsis
#line 220 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = PyList_New(0); }
#line 1263 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 30: // class_funcs: funcdefs
#line 221 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1269 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 31: // funcdefs: funcdefs constantdef
#line 225 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                         { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1275 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 32: // funcdefs: funcdefs alias_or_constant
#line 226 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                               {
      PyObject* tmp = ctx->Call(kNewAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      (yylhs.value.obj) = AppendList((yystack_[1].value.obj), tmp);
    }
#line 1285 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 33: // funcdefs: funcdefs funcdef
#line 231 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1291 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 34: // funcdefs: funcdefs class_if_stmt
#line 232 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1301 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 35: // funcdefs: funcdefs classdef
#line 237 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1307 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 36: // funcdefs: %empty
#line 238 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1313 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 37: // if_stmt: if_and_elifs else_cond ':' INDENT alldefs DEDENT
#line 243 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                     {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1321 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 38: // if_stmt: if_and_elifs
#line 246 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1327 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 39: // if_and_elifs: if_cond ':' INDENT alldefs DEDENT
#line 251 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                      {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1335 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 40: // if_and_elifs: if_and_elifs elif_cond ':' INDENT alldefs DEDENT
#line 255 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                     {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1343 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 41: // class_if_stmt: class_if_and_elifs else_cond ':' INDENT funcdefs DEDENT
#line 268 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                            {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1351 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 42: // class_if_stmt: class_if_and_elifs
#line 271 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1357 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 43: // class_if_and_elifs: if_cond ':' INDENT funcdefs DEDENT
#line 276 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1365 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 44: // class_if_and_elifs: class_if_and_elifs elif_cond ':' INDENT funcdefs DEDENT
#line 280 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                            {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1373 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 45: // if_cond: IF condition
#line 292 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = ctx->Call(kIfBegin, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1379 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 46: // elif_cond: ELIF condition
#line 296 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                   { (yylhs.value.obj) = ctx->Call(kIfElif, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1385 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 47: // else_cond: ELSE
#line 300 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = ctx->Call(kIfElse, "()"); CHECK((yylhs.value.obj), yylhs.location); }
#line 1391 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 48: // condition: dotted_name condition_op STRING
#line 304 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1399 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 49: // condition: dotted_name condition_op version_tuple
#line 307 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                           {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1407 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 50: // condition: dotted_name '[' getitem_key ']' condition_op NUMBER
#line 310 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                        {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1415 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 51: // condition: dotted_name '[' getitem_key ']' condition_op version_tuple
#line 313 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                               {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1423 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 52: // condition: condition AND condition
#line 316 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                            { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "and", (yystack_[0].value.obj)); }
#line 1429 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 53: // condition: condition OR condition
#line 317 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "or", (yystack_[0].value.obj)); }
#line 1435 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 54: // condition: '(' condition ')'
#line 318 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1441 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 55: // version_tuple: '(' NUMBER ',' ')'
#line 322 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = Py_BuildValue("(N)", (yystack_[2].value.obj)); }
#line 1447 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 56: // version_tuple: '(' NUMBER ',' NUMBER ')'
#line 323 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                              { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 1453 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 57: // version_tuple: '(' NUMBER ',' NUMBER ',' NUMBER ')'
#line 324 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                         {
      (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj));
    }
#line 1461 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 58: // condition_op: '<'
#line 330 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "<"; }
#line 1467 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 59: // condition_op: '>'
#line 331 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = ">"; }
#line 1473 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 60: // condition_op: LE
#line 332 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "<="; }
#line 1479 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 61: // condition_op: GE
#line 333 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = ">="; }
#line 1485 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 62: // condition_op: EQ
#line 334 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "=="; }
#line 1491 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 63: // condition_op: NE
#line 335 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "!="; }
#line 1497 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 64: // constantdef: NAME '=' NUMBER
#line 339 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1506 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 65: // constantdef: NAME '=' STRING
#line 343 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1515 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 66: // constantdef: NAME '=' type_tuple_literal
#line 347 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1524 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 67: // constantdef: NAME '=' ELLIPSIS
#line 351 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kAnything));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1533 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 68: // constantdef: NAME '=' ELLIPSIS TYPECOMMENT type maybe_type_ignore
#line 355 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                         {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1542 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 69: // constantdef: NAME ':' type maybe_type_ignore
#line 359 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1551 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 70: // constantdef: NAME ':' type '=' ELLIPSIS maybe_type_ignore
#line 363 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                 {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[3].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1560 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 71: // constantdef: TYPEDDICT ':' type maybe_type_ignore
#line 367 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                         {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", PyString_FromString("TypedDict"), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1569 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 72: // constantdef: TYPEDDICT ':' type '=' ELLIPSIS maybe_type_ignore
#line 371 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                      {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", PyString_FromString("TypedDict"), (yystack_[3].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1578 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 73: // importdef: IMPORT import_items maybe_type_ignore
#line 378 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                          {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(ON)", Py_None, (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1587 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 74: // importdef: FROM import_name IMPORT from_list maybe_type_ignore
#line 382 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                        {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1596 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 75: // importdef: FROM '.' IMPORT from_list maybe_type_ignore
#line 386 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                {
      // Special-case "from . import" and pass in a __PACKAGE__ token that
      // the Python parser code will rewrite to the current package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PACKAGE__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1607 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 76: // importdef: FROM '.' '.' IMPORT from_list maybe_type_ignore
#line 392 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                    {
      // Special-case "from .. import" and pass in a __PARENT__ token that
      // the Python parser code will rewrite to the parent package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PARENT__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1618 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 77: // import_items: import_items ',' import_item
#line 401 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                 { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1624 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 78: // import_items: import_item
#line 402 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1630 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 79: // import_item: dotted_name
#line 406 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1636 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 80: // import_item: dotted_name AS NAME
#line 407 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                        { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1642 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 81: // import_name: dotted_name
#line 412 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1648 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 82: // import_name: '.' import_name
#line 413 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = PyString_FromFormat(".%s", PyString_AsString((yystack_[0].value.obj)));
      Py_DECREF((yystack_[0].value.obj));
    }
#line 1657 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 83: // from_list: from_items
#line 420 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1663 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 84: // from_list: '(' from_items ')'
#line 421 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1669 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 85: // from_list: '(' from_items ',' ')'
#line 422 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1675 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 86: // from_items: from_items ',' from_item
#line 426 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                             { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1681 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 87: // from_items: from_item
#line 427 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1687 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 88: // from_item: NAME
#line 431 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1693 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 89: // from_item: NAMEDTUPLE
#line 432 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               {
      (yylhs.value.obj) = PyString_FromString("NamedTuple");
    }
#line 1701 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 90: // from_item: COLL_NAMEDTUPLE
#line 435 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = PyString_FromString("namedtuple");
    }
#line 1709 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 91: // from_item: NEWTYPE
#line 438 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            {
      (yylhs.value.obj) = PyString_FromString("NewType");
    }
#line 1717 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 92: // from_item: TYPEDDICT
#line 441 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              {
      (yylhs.value.obj) = PyString_FromString("TypedDict");
    }
#line 1725 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 93: // from_item: TYPEVAR
#line 444 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            {
      (yylhs.value.obj) = PyString_FromString("TypeVar");
    }
#line 1733 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 94: // from_item: '*'
#line 447 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        {
      (yylhs.value.obj) = PyString_FromString("*");
    }
#line 1741 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 95: // from_item: NAME AS NAME
#line 450 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1747 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 96: // from_item: NEWTYPE AS NEWTYPE
#line 451 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = PyString_FromString("NewType"); }
#line 1753 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 97: // alias_or_constant: NAME '=' type maybe_type_ignore
#line 455 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 1759 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 98: // alias_or_constant: NAME '=' '[' maybe_string_list ']' maybe_type_ignore
#line 456 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                         { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[5].value.obj), (yystack_[2].value.obj)); }
#line 1765 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 99: // maybe_string_list: string_list maybe_comma
#line 460 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                            { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1771 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 100: // maybe_string_list: %empty
#line 461 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1777 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 101: // string_list: string_list ',' STRING
#line 465 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1783 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 102: // string_list: STRING
#line 466 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1789 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 103: // typevardef: NAME '=' TYPEVAR '(' STRING typevar_args ')'
#line 470 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                 {
      (yylhs.value.obj) = ctx->Call(kAddTypeVar, "(NNN)", (yystack_[6].value.obj), (yystack_[2].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1798 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 104: // typevar_args: %empty
#line 477 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = Py_BuildValue("(OO)", Py_None, Py_None); }
#line 1804 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 105: // typevar_args: ',' type_list
#line 478 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NO)", (yystack_[0].value.obj), Py_None); }
#line 1810 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 106: // typevar_args: ',' typevar_kwargs
#line 479 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = Py_BuildValue("(ON)", Py_None, (yystack_[0].value.obj)); }
#line 1816 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 107: // typevar_args: ',' type_list ',' typevar_kwargs
#line 480 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                     { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1822 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 108: // typevar_kwargs: typevar_kwargs ',' typevar_kwarg
#line 484 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                     { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1828 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 109: // typevar_kwargs: typevar_kwarg
#line 485 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1834 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 110: // typevar_kwarg: NAME '=' type
#line 489 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1840 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 111: // typevar_kwarg: NAME '=' STRING
#line 491 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1846 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 112: // funcdef: decorators maybe_async DEF funcname '(' maybe_type_ignore params ')' return maybe_body
#line 496 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               {
      (yylhs.value.obj) = ctx->Call(kNewFunction, "(NONNNN)", (yystack_[9].value.obj), (yystack_[8].value.obj), (yystack_[6].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj));
      // Decorators is nullable and messes up the location tracking by
      // using the previous symbol as the start location for this production,
      // which is very misleading.  It is better to ignore decorators and
      // pretend the production started with DEF.  Even when decorators are
      // present the error line will be close enough to be helpful.
      yylhs.location.begin = yystack_[7].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1861 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 113: // funcname: NAME
#line 509 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1867 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 114: // funcname: COLL_NAMEDTUPLE
#line 510 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = PyString_FromString("namedtuple"); }
#line 1873 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 115: // funcname: NEWTYPE
#line 511 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyString_FromString("NewType"); }
#line 1879 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 116: // funcname: TYPEDDICT
#line 512 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              { (yylhs.value.obj) = PyString_FromString("TypedDict"); }
#line 1885 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 117: // decorators: decorators decorator
#line 516 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                         { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1891 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 118: // decorators: %empty
#line 517 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1897 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 119: // decorator: '@' dotted_name maybe_type_ignore
#line 521 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                      { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1903 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 120: // maybe_async: ASYNC
#line 525 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
          { (yylhs.value.obj) = Py_True; }
#line 1909 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 121: // maybe_async: %empty
#line 526 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = Py_False; }
#line 1915 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 122: // params: param_list maybe_comma
#line 530 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1921 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 123: // params: %empty
#line 531 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1927 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 124: // param_list: param_list ',' maybe_type_ignore param
#line 543 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                           { (yylhs.value.obj) = AppendList((yystack_[3].value.obj), (yystack_[0].value.obj)); }
#line 1933 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 125: // param_list: param
#line 544 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
          { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1939 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 126: // param: NAME param_type param_default
#line 548 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                  { (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[2].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1945 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 127: // param: '*'
#line 549 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.obj) = Py_BuildValue("(sOO)", "*", Py_None, Py_None); }
#line 1951 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 128: // param: param_star_name param_type
#line 550 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                               { (yylhs.value.obj) = Py_BuildValue("(NNO)", (yystack_[1].value.obj), (yystack_[0].value.obj), Py_None); }
#line 1957 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 129: // param: ELLIPSIS
#line 551 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1963 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 130: // param_type: ':' type
#line 555 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1969 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 131: // param_type: %empty
#line 556 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1975 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 132: // param_default: '=' NAME
#line 560 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1981 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 133: // param_default: '=' NUMBER
#line 561 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1987 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 134: // param_default: '=' ELLIPSIS
#line 562 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1993 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 135: // param_default: %empty
#line 563 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1999 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 136: // param_star_name: '*' NAME
#line 567 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = PyString_FromFormat("*%s", PyString_AsString((yystack_[0].value.obj))); }
#line 2005 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 137: // param_star_name: '*' '*' NAME
#line 568 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = PyString_FromFormat("**%s", PyString_AsString((yystack_[0].value.obj))); }
#line 2011 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 138: // return: ARROW type
#line 572 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2017 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 139: // return: %empty
#line 573 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 2023 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 140: // typeignore: TYPECOMMENT NAME
#line 577 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { Py_DecRef((yystack_[0].value.obj)); }
#line 2029 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 141: // typeignore: TYPECOMMENT NAME '[' maybe_type_list ']'
#line 578 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                             {
      Py_DecRef((yystack_[3].value.obj));
      Py_DecRef((yystack_[1].value.obj));
    }
#line 2038 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 142: // maybe_body: ':' typeignore INDENT body DEDENT
#line 585 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                      { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2044 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 143: // maybe_body: ':' INDENT body DEDENT
#line 586 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2050 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 144: // maybe_body: empty_body
#line 587 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = PyList_New(0); }
#line 2056 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 152: // body: body body_stmt
#line 601 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                   { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 2062 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 153: // body: body_stmt
#line 602 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2068 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 154: // body_stmt: NAME '=' type
#line 606 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2074 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 155: // body_stmt: RAISE type
#line 607 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2080 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 156: // body_stmt: RAISE type '(' ')'
#line 608 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2086 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 157: // type_parameters: type_parameters ',' type_parameter
#line 612 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2092 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 158: // type_parameters: type_parameter
#line 613 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                   { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2098 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 159: // type_parameter: type
#line 617 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2104 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 160: // type_parameter: ELLIPSIS
#line 618 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 2110 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 161: // type_parameter: NUMBER
#line 620 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2116 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 162: // type_parameter: STRING
#line 621 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2122 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 163: // type_parameter: '[' maybe_type_list ']'
#line 623 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                            {
      (yylhs.value.obj) = ctx->Call(kNewType, "(sN)", "tuple", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2131 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 164: // maybe_type_list: type_list maybe_comma
#line 630 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                          { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2137 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 165: // maybe_type_list: %empty
#line 631 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 2143 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 166: // type_list: type_list ',' type
#line 635 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2149 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 167: // type_list: type
#line 636 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2155 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 168: // type: dotted_name
#line 640 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                {
      (yylhs.value.obj) = ctx->Call(kNewType, "(N)", (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2164 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 169: // type: dotted_name '[' '(' ')' ']'
#line 644 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[4].value.obj), PyList_New(0));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2173 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 170: // type: dotted_name '[' type_parameters maybe_comma ']'
#line 648 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2182 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 171: // type: NAMEDTUPLE '(' STRING ',' named_tuple_fields maybe_comma ')'
#line 652 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                                 {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2191 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 172: // type: COLL_NAMEDTUPLE '(' STRING ',' coll_named_tuple_fields maybe_comma ')'
#line 656 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                                           {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2200 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 173: // type: NEWTYPE '(' STRING ',' type maybe_comma ')'
#line 660 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                {
      (yylhs.value.obj) = ctx->Call(kNewNewType, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2209 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 174: // type: TYPEDDICT '(' STRING ',' typed_dict_fields maybe_typed_dict_kwarg ')'
#line 664 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                                          {
      (yylhs.value.obj) = ctx->Call(kNewTypedDict, "(NNN)", (yystack_[4].value.obj), (yystack_[2].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2218 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 175: // type: '(' type ')'
#line 668 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2224 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 176: // type: type AND type
#line 669 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = ctx->Call(kNewIntersectionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2230 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 177: // type: type OR type
#line 670 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = ctx->Call(kNewUnionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2236 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 178: // type: '?'
#line 671 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 2242 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 179: // type: NOTHING
#line 672 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = ctx->Value(kNothing); }
#line 2248 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 180: // named_tuple_fields: '[' named_tuple_field_list maybe_comma ']'
#line 676 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                               { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2254 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 181: // named_tuple_fields: '[' ']'
#line 677 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyList_New(0); }
#line 2260 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 182: // named_tuple_field_list: named_tuple_field_list ',' named_tuple_field
#line 681 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                 { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2266 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 183: // named_tuple_field_list: named_tuple_field
#line 682 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2272 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 184: // named_tuple_field: '(' STRING ',' type maybe_comma ')'
#line 686 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                         { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj)); }
#line 2278 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 187: // coll_named_tuple_fields: '[' coll_named_tuple_field_list maybe_comma ']'
#line 695 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2284 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 188: // coll_named_tuple_fields: '[' ']'
#line 696 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyList_New(0); }
#line 2290 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 189: // coll_named_tuple_field_list: coll_named_tuple_field_list ',' coll_named_tuple_field
#line 700 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                           {
      (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj));
    }
#line 2298 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 190: // coll_named_tuple_field_list: coll_named_tuple_field
#line 703 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2304 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 191: // coll_named_tuple_field: STRING
#line 707 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[0].value.obj), ctx->Value(kAnything)); }
#line 2310 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 192: // typed_dict_fields: '{' typed_dict_field_dict maybe_comma '}'
#line 711 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                              { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2316 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 193: // typed_dict_fields: '{' '}'
#line 712 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyDict_New(); }
#line 2322 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 194: // typed_dict_field_dict: typed_dict_field_dict ',' typed_dict_field
#line 716 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                               {
      PyDict_Update((yystack_[2].value.obj), (yystack_[0].value.obj));
      (yylhs.value.obj) = (yystack_[2].value.obj);
      Py_DECREF((yystack_[0].value.obj));
    }
#line 2332 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 195: // typed_dict_field_dict: typed_dict_field
#line 721 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2338 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 196: // typed_dict_field: STRING ':' NAME
#line 725 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = Py_BuildValue("{N: N}", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2344 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 197: // maybe_typed_dict_kwarg: ',' NAME '=' type maybe_comma
#line 729 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 2350 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 198: // maybe_typed_dict_kwarg: maybe_comma
#line 730 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = Py_None; }
#line 2356 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 199: // type_tuple_elements: type_tuple_elements ',' type
#line 737 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                 { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2362 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 200: // type_tuple_elements: type ',' type
#line 738 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2368 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 201: // type_tuple_literal: '(' type_tuple_elements maybe_comma ')'
#line 747 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                            {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2377 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 202: // type_tuple_literal: '(' type ',' ')'
#line 752 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2386 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 203: // type_tuple_literal: type ','
#line 758 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             {
      Py_DECREF((yystack_[1].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2395 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 204: // dotted_name: NAME
#line 765 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2401 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 205: // dotted_name: dotted_name '.' NAME
#line 766 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                         {
#if PY_MAJOR_VERSION >= 3
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), DOT_STRING);
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), (yystack_[0].value.obj));
      Py_DECREF((yystack_[0].value.obj));
#else
      PyString_Concat(&(yystack_[2].value.obj), DOT_STRING);
      PyString_ConcatAndDel(&(yystack_[2].value.obj), (yystack_[0].value.obj));
#endif
      (yylhs.value.obj) = (yystack_[2].value.obj);
    }
#line 2417 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 206: // getitem_key: NUMBER
#line 780 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2423 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 207: // getitem_key: maybe_number ':' maybe_number
#line 781 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                  {
      PyObject* slice = PySlice_New((yystack_[2].value.obj), (yystack_[0].value.obj), NULL);
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2433 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 208: // getitem_key: maybe_number ':' maybe_number ':' maybe_number
#line 786 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                   {
      PyObject* slice = PySlice_New((yystack_[4].value.obj), (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2443 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 209: // maybe_number: NUMBER
#line 794 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2449 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 210: // maybe_number: %empty
#line 795 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = NULL; }
#line 2455 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;


#line 2459 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

            default:
              break;
            }
        }
#if YY_EXCEPTIONS
      catch (const syntax_error& yyexc)
        {
          YYCDEBUG << "Caught exception: " << yyexc.what() << '\n';
          error (yyexc);
          YYERROR;
        }
#endif // YY_EXCEPTIONS
      YY_SYMBOL_PRINT ("-> $$ =", yylhs);
      yypop_ (yylen);
      yylen = 0;

      // Shift the result of the reduction.
      yypush_ (YY_NULLPTR, YY_MOVE (yylhs));
    }
    goto yynewstate;


  /*--------------------------------------.
  | yyerrlab -- here on detecting error.  |
  `--------------------------------------*/
  yyerrlab:
    // If not already recovering from an error, report this error.
    if (!yyerrstatus_)
      {
        ++yynerrs_;
        context yyctx (*this, yyla);
        std::string msg = yysyntax_error_ (yyctx);
        error (yyla.location, YY_MOVE (msg));
      }


    yyerror_range[1].location = yyla.location;
    if (yyerrstatus_ == 3)
      {
        /* If just tried and failed to reuse lookahead token after an
           error, discard it.  */

        // Return failure if at end of input.
        if (yyla.kind () == symbol_kind::S_YYEOF)
          YYABORT;
        else if (!yyla.empty ())
          {
            yy_destroy_ ("Error: discarding", yyla);
            yyla.clear ();
          }
      }

    // Else will try to reuse lookahead token after shifting the error token.
    goto yyerrlab1;


  /*---------------------------------------------------.
  | yyerrorlab -- error raised explicitly by YYERROR.  |
  `---------------------------------------------------*/
  yyerrorlab:
    /* Pacify compilers when the user code never invokes YYERROR and
       the label yyerrorlab therefore never appears in user code.  */
    if (false)
      YYERROR;

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYERROR.  */
    yypop_ (yylen);
    yylen = 0;
    YY_STACK_PRINT ();
    goto yyerrlab1;


  /*-------------------------------------------------------------.
  | yyerrlab1 -- common code for both syntax error and YYERROR.  |
  `-------------------------------------------------------------*/
  yyerrlab1:
    yyerrstatus_ = 3;   // Each real token shifted decrements this.
    // Pop stack until we find a state that shifts the error token.
    for (;;)
      {
        yyn = yypact_[+yystack_[0].state];
        if (!yy_pact_value_is_default_ (yyn))
          {
            yyn += symbol_kind::S_YYerror;
            if (0 <= yyn && yyn <= yylast_
                && yycheck_[yyn] == symbol_kind::S_YYerror)
              {
                yyn = yytable_[yyn];
                if (0 < yyn)
                  break;
              }
          }

        // Pop the current state because it cannot handle the error token.
        if (yystack_.size () == 1)
          YYABORT;

        yyerror_range[1].location = yystack_[0].location;
        yy_destroy_ ("Error: popping", yystack_[0]);
        yypop_ ();
        YY_STACK_PRINT ();
      }
    {
      stack_symbol_type error_token;

      yyerror_range[2].location = yyla.location;
      YYLLOC_DEFAULT (error_token.location, yyerror_range, 2);

      // Shift the error token.
      error_token.state = state_type (yyn);
      yypush_ ("Shifting", YY_MOVE (error_token));
    }
    goto yynewstate;


  /*-------------------------------------.
  | yyacceptlab -- YYACCEPT comes here.  |
  `-------------------------------------*/
  yyacceptlab:
    yyresult = 0;
    goto yyreturn;


  /*-----------------------------------.
  | yyabortlab -- YYABORT comes here.  |
  `-----------------------------------*/
  yyabortlab:
    yyresult = 1;
    goto yyreturn;


  /*-----------------------------------------------------.
  | yyreturn -- parsing is finished, return the result.  |
  `-----------------------------------------------------*/
  yyreturn:
    if (!yyla.empty ())
      yy_destroy_ ("Cleanup: discarding lookahead", yyla);

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYABORT or YYACCEPT.  */
    yypop_ (yylen);
    YY_STACK_PRINT ();
    while (1 < yystack_.size ())
      {
        yy_destroy_ ("Cleanup: popping", yystack_[0]);
        yypop_ ();
      }

    return yyresult;
  }
#if YY_EXCEPTIONS
    catch (...)
      {
        YYCDEBUG << "Exception caught: cleaning lookahead and stack\n";
        // Do not try to display the values of the reclaimed symbols,
        // as their printers might throw an exception.
        if (!yyla.empty ())
          yy_destroy_ (YY_NULLPTR, yyla);

        while (1 < yystack_.size ())
          {
            yy_destroy_ (YY_NULLPTR, yystack_[0]);
            yypop_ ();
          }
        throw;
      }
#endif // YY_EXCEPTIONS
  }

  void
  parser::error (const syntax_error& yyexc)
  {
    error (yyexc.location, yyexc.what ());
  }

  /* Return YYSTR after stripping away unnecessary quotes and
     backslashes, so that it's suitable for yyerror.  The heuristic is
     that double-quoting is unnecessary unless the string contains an
     apostrophe, a comma, or backslash (other than backslash-backslash).
     YYSTR is taken from yytname.  */
  std::string
  parser::yytnamerr_ (const char *yystr)
  {
    if (*yystr == '"')
      {
        std::string yyr;
        char const *yyp = yystr;

        for (;;)
          switch (*++yyp)
            {
            case '\'':
            case ',':
              goto do_not_strip_quotes;

            case '\\':
              if (*++yyp != '\\')
                goto do_not_strip_quotes;
              else
                goto append;

            append:
            default:
              yyr += *yyp;
              break;

            case '"':
              return yyr;
            }
      do_not_strip_quotes: ;
      }

    return yystr;
  }

  std::string
  parser::symbol_name (symbol_kind_type yysymbol)
  {
    return yytnamerr_ (yytname_[yysymbol]);
  }



  // parser::context.
  parser::context::context (const parser& yyparser, const symbol_type& yyla)
    : yyparser_ (yyparser)
    , yyla_ (yyla)
  {}

  int
  parser::context::expected_tokens (symbol_kind_type yyarg[], int yyargn) const
  {
    // Actual number of expected tokens
    int yycount = 0;

    int yyn = yypact_[+yyparser_.yystack_[0].state];
    if (!yy_pact_value_is_default_ (yyn))
      {
        /* Start YYX at -YYN if negative to avoid negative indexes in
           YYCHECK.  In other words, skip the first -YYN actions for
           this state because they are default actions.  */
        int yyxbegin = yyn < 0 ? -yyn : 0;
        // Stay within bounds of both yycheck and yytname.
        int yychecklim = yylast_ - yyn + 1;
        int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
        for (int yyx = yyxbegin; yyx < yyxend; ++yyx)
          if (yycheck_[yyx + yyn] == yyx && yyx != symbol_kind::S_YYerror
              && !yy_table_value_is_error_ (yytable_[yyx + yyn]))
            {
              if (!yyarg)
                ++yycount;
              else if (yycount == yyargn)
                return 0;
              else
                yyarg[yycount++] = YY_CAST (symbol_kind_type, yyx);
            }
      }

    if (yyarg && yycount == 0 && 0 < yyargn)
      yyarg[0] = symbol_kind::S_YYEMPTY;
    return yycount;
  }



  int
  parser::yy_syntax_error_arguments_ (const context& yyctx,
                                                 symbol_kind_type yyarg[], int yyargn) const
  {
    /* There are many possibilities here to consider:
       - If this state is a consistent state with a default action, then
         the only way this function was invoked is if the default action
         is an error action.  In that case, don't check for expected
         tokens because there are none.
       - The only way there can be no lookahead present (in yyla) is
         if this state is a consistent state with a default action.
         Thus, detecting the absence of a lookahead is sufficient to
         determine that there is no unexpected or expected token to
         report.  In that case, just report a simple "syntax error".
       - Don't assume there isn't a lookahead just because this state is
         a consistent state with a default action.  There might have
         been a previous inconsistent state, consistent state with a
         non-default action, or user semantic action that manipulated
         yyla.  (However, yyla is currently not documented for users.)
       - Of course, the expected token list depends on states to have
         correct lookahead information, and it depends on the parser not
         to perform extra reductions after fetching a lookahead from the
         scanner and before detecting a syntax error.  Thus, state merging
         (from LALR or IELR) and default reductions corrupt the expected
         token list.  However, the list is correct for canonical LR with
         one exception: it will still contain any token that will not be
         accepted due to an error action in a later state.
    */

    if (!yyctx.lookahead ().empty ())
      {
        if (yyarg)
          yyarg[0] = yyctx.token ();
        int yyn = yyctx.expected_tokens (yyarg ? yyarg + 1 : yyarg, yyargn - 1);
        return yyn + 1;
      }
    return 0;
  }

  // Generate an error message.
  std::string
  parser::yysyntax_error_ (const context& yyctx) const
  {
    // Its maximum.
    enum { YYARGS_MAX = 5 };
    // Arguments of yyformat.
    symbol_kind_type yyarg[YYARGS_MAX];
    int yycount = yy_syntax_error_arguments_ (yyctx, yyarg, YYARGS_MAX);

    char const* yyformat = YY_NULLPTR;
    switch (yycount)
      {
#define YYCASE_(N, S)                         \
        case N:                               \
          yyformat = S;                       \
        break
      default: // Avoid compiler warnings.
        YYCASE_ (0, YY_("syntax error"));
        YYCASE_ (1, YY_("syntax error, unexpected %s"));
        YYCASE_ (2, YY_("syntax error, unexpected %s, expecting %s"));
        YYCASE_ (3, YY_("syntax error, unexpected %s, expecting %s or %s"));
        YYCASE_ (4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
        YYCASE_ (5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
#undef YYCASE_
      }

    std::string yyres;
    // Argument number.
    std::ptrdiff_t yyi = 0;
    for (char const* yyp = yyformat; *yyp; ++yyp)
      if (yyp[0] == '%' && yyp[1] == 's' && yyi < yycount)
        {
          yyres += symbol_name (yyarg[yyi++]);
          ++yyp;
        }
      else
        yyres += *yyp;
    return yyres;
  }


  const short parser::yypact_ninf_ = -347;

  const short parser::yytable_ninf_ = -210;

  const short
  parser::yypact_[] =
  {
     -17,  -347,    73,    87,   422,   117,  -347,  -347,   214,    37,
     128,    10,    84,  -347,  -347,   187,   121,  -347,  -347,  -347,
    -347,  -347,    36,  -347,    43,   169,  -347,    37,   256,   428,
      90,  -347,    88,    17,   148,   160,    43,  -347,    37,   126,
     171,   180,  -347,   226,   128,  -347,   234,  -347,   223,   239,
     246,   248,    43,  -347,   338,   212,  -347,  -347,   303,   216,
      43,   348,   146,  -347,   274,    37,    37,  -347,  -347,  -347,
    -347,   359,  -347,  -347,   363,    77,   371,   128,  -347,  -347,
     372,   362,    26,  -347,   362,   388,   256,   345,   349,  -347,
    -347,   352,   -11,   409,   391,   392,   398,   399,   293,    43,
      43,   378,  -347,   199,   401,    43,   242,   387,  -347,   368,
     390,  -347,  -347,  -347,   413,  -347,   375,   400,   407,  -347,
    -347,   433,  -347,   403,  -347,  -347,   427,  -347,  -347,   432,
    -347,  -347,   395,  -347,   416,   414,  -347,   362,    27,   416,
     435,  -347,  -347,  -347,   151,   271,   418,  -347,  -347,  -347,
    -347,  -347,   423,   424,   425,   426,   429,  -347,   453,  -347,
     416,  -347,  -347,  -347,   276,    43,   431,  -347,   307,   439,
      18,   312,    43,   441,   416,   475,  -347,   446,   477,   443,
      43,   480,   461,   309,  -347,   395,   416,  -347,   416,   225,
     397,  -347,   445,   223,   248,  -347,   323,  -347,   307,   416,
     416,   447,   450,    43,   437,  -347,   451,   452,   448,   307,
     211,   454,   281,   457,  -347,  -347,   307,   307,  -347,  -347,
    -347,    33,  -347,   456,    48,   455,  -347,  -347,  -347,   369,
    -347,  -347,  -347,  -347,  -347,    43,  -347,   322,   296,    22,
      82,   459,     9,   459,   156,     4,   460,  -347,  -347,    43,
    -347,  -347,  -347,   462,   464,  -347,   465,  -347,  -347,  -347,
     477,   330,  -347,  -347,  -347,   307,  -347,  -347,  -347,   100,
    -347,   416,   469,  -347,    23,   463,   467,  -347,   469,   495,
    -347,   468,  -347,  -347,   470,  -347,  -347,   471,  -347,   473,
     474,   478,  -347,   476,  -347,   506,  -347,   479,   307,   334,
     510,   281,  -347,  -347,   512,    20,   485,    99,  -347,  -347,
      43,   481,  -347,   516,   494,   145,  -347,  -347,   483,   486,
     482,  -347,   520,   484,  -347,  -347,   524,   523,   487,   489,
    -347,  -347,   307,   462,  -347,   464,   492,   498,  -347,   286,
    -347,  -347,   187,   496,  -347,  -347,  -347,   307,   197,  -347,
    -347,    43,   497,    22,    43,  -347,  -347,  -347,  -347,  -347,
    -347,  -347,    43,  -347,  -347,   241,   499,   500,   502,  -347,
    -347,  -347,   307,   420,  -347,  -347,  -347,   156,   156,   507,
     508,  -347,   361,   434,   416,   503,  -347,  -347,  -347,   125,
     504,    43,   505,    89,  -347,   509,   421,  -347,  -347,  -347,
     175,   206,  -347,    43,   253,  -347,  -347,  -347,  -347,   132,
     513,  -347,  -347,   307,   511,  -347,  -347,  -347
  };

  const unsigned char
  parser::yydefact_[] =
  {
      12,    12,     0,     0,   118,     0,     1,     2,     0,     0,
       0,     0,     0,     9,    11,    38,     0,     5,     7,     8,
      10,     6,   121,     3,     0,     0,   204,     0,    45,     0,
      14,    78,    79,     0,     0,    81,     0,    47,     0,     0,
       0,     0,   120,     0,     0,   117,     0,   179,     0,     0,
       0,     0,     0,   178,    14,   168,    64,    65,     0,    67,
       0,   100,    14,    66,     0,     0,     0,    62,    63,    60,
      61,   210,    58,    59,     0,     0,     0,     0,    73,    13,
       0,     0,     0,    82,     0,    14,    46,     0,     0,    12,
      16,    19,    14,     0,     0,     0,     0,     0,     0,     0,
       0,     0,    69,     0,     0,     0,     0,   186,   102,     0,
     186,   203,    97,    54,    53,    52,   206,     0,     0,   205,
      48,     0,    49,   140,    77,    80,    88,    89,    90,    91,
      92,    93,     0,    94,    14,    83,    87,     0,     0,    14,
       0,    71,    12,    12,   118,     0,     0,   119,   113,   114,
     115,   116,     0,     0,     0,     0,     0,   175,   177,   176,
      14,   161,   162,   160,     0,   165,   186,   158,   159,   104,
      14,     0,   185,     0,    14,   185,    99,     0,   210,     0,
     165,     0,     0,     0,    75,     0,    14,    74,    14,   118,
     118,    39,   204,    24,    25,    18,     0,    21,    22,    14,
      14,     0,     0,     0,     0,    70,     0,     0,   186,   167,
     185,     0,     0,     0,    68,   202,   200,   199,   201,    98,
     101,     0,   209,   207,     0,     0,    95,    96,    84,     0,
      86,    76,    72,    40,    37,     0,    17,     0,     0,   123,
       0,   186,     0,   186,   186,     0,   186,   169,   163,   185,
     164,   157,   170,   204,   106,   109,   105,   103,    50,    51,
     210,     0,    55,   141,    85,    23,    20,   211,   212,    36,
      15,    14,   131,   129,   127,     0,   186,   125,   131,     0,
     181,   186,   183,   185,     0,   191,   188,   186,   190,     0,
       0,     0,   193,   186,   195,   185,   198,     0,   166,     0,
       0,     0,   208,    56,     0,    36,     0,   118,    29,    26,
       0,   135,   136,     0,   139,    14,   122,   128,     0,   185,
       0,   171,   185,     0,   172,   173,     0,   185,     0,     0,
     174,   111,   110,     0,   108,   107,     0,     0,    27,     0,
      35,    34,    42,     0,    31,    32,    33,   130,     0,   126,
     137,     0,   151,     0,     0,   182,   180,   189,   187,   196,
     194,   192,     0,    57,    28,     0,     0,     0,     0,   132,
     133,   134,   138,     0,   112,   144,   124,   186,   186,     0,
       0,    36,     0,     0,   145,     0,   197,    36,    36,   118,
       0,     0,     0,     0,   153,     0,     0,   147,   146,   184,
     118,   118,    43,     0,   155,   150,   143,   152,   149,     0,
       0,    44,    41,   154,     0,   142,   148,   156
  };

  const short
  parser::yypgoto_[] =
  {
    -347,  -347,   542,   -85,   -44,  -304,  -347,  -347,  -347,   308,
    -347,   243,   -71,  -347,  -347,  -347,  -347,  -301,   205,   208,
      80,   331,   374,  -296,  -347,  -347,   488,   543,   -77,   430,
    -170,  -291,  -347,  -347,  -347,  -347,   252,   255,  -288,  -347,
    -347,  -347,  -347,  -347,  -347,   203,   279,  -347,  -347,  -347,
    -346,  -347,  -347,   162,  -232,  -347,   350,   379,   351,   -24,
    -347,  -347,   245,  -105,  -347,  -347,   244,  -347,  -347,   240,
    -347,  -347,  -347,    12,  -347,  -176,  -230
  };

  const short
  parser::yydefgoto_[] =
  {
      -1,     2,     3,     4,    78,    13,    91,   146,   196,   197,
     270,   306,   307,    14,    15,   341,   342,    16,    39,    40,
      28,   122,    75,    17,    18,    30,    31,    83,   134,   135,
     136,    19,   109,   110,    20,   213,   254,   255,    21,   152,
      22,    45,    46,   275,   276,   277,   311,   349,   278,   352,
      79,   374,   375,   393,   394,   166,   167,   207,   208,   209,
     241,   281,   282,   173,   243,   287,   288,   246,   293,   294,
     297,   107,    63,    55,   117,   118,   308
  };

  const short
  parser::yytable_[] =
  {
      54,    62,   223,   340,   144,   176,   343,   139,   271,   291,
     102,   344,    85,    26,   285,   230,   345,     1,   112,   346,
      26,    29,    32,    35,    76,   272,   312,   383,    98,    26,
      26,    99,   100,    81,    74,   267,   106,   258,   398,    29,
      26,   141,   137,    42,    43,    35,    26,   268,   147,   273,
      29,   286,   261,    76,   292,    33,    92,   189,   190,   230,
     186,   211,    82,    47,    48,    49,    50,    51,   274,   313,
     121,   138,   138,     6,    27,   158,   159,    29,    29,   168,
      52,   170,   120,    44,   302,   340,   262,     7,   343,    32,
     184,    53,   390,   344,    35,   187,   340,   340,   345,   343,
     343,   346,   339,   250,   344,   344,    80,    64,   391,   345,
     345,     9,   346,   346,   121,   267,   205,    23,    86,   279,
      36,   198,   406,    12,   280,    76,   214,   268,   339,    77,
     219,    26,   -30,    74,   305,   390,   284,     9,   289,   290,
      98,   296,   231,   384,   232,   114,   115,   216,   217,    12,
      35,   391,   395,   397,     8,   238,   239,    41,   402,    99,
     100,   407,    87,     9,    84,   415,   410,    10,    11,    99,
     100,   316,    26,    56,    57,    12,   320,   407,   339,   244,
      76,    76,   323,  -185,   191,   111,   168,     9,   328,    47,
      48,    49,    50,    51,    58,   283,    59,    37,    38,    12,
     369,   370,    26,   161,   162,    74,    60,    88,   411,   339,
      61,   265,    89,   198,    26,   161,   162,    53,     9,    47,
      48,    49,    50,    51,   371,   298,   163,   309,     8,    90,
      12,    47,    48,    49,    50,    51,   164,     9,   163,   412,
     165,    10,    11,    93,    26,    56,    57,    53,    52,    12,
      24,   105,   165,   103,    25,    99,   100,    74,   233,    53,
      94,    47,    48,    49,    50,    51,    99,   100,    59,    65,
      66,   353,   385,   386,   192,   332,    95,   298,    60,    26,
     157,   171,    61,    96,   253,    97,   347,    65,    66,    53,
     414,    47,   193,    49,    50,   194,    47,    48,    49,    50,
      51,    47,    48,    49,    50,    51,    99,   100,    52,   195,
     389,   267,   113,    52,   206,    26,   400,   401,    52,    53,
      99,   100,    24,   268,    53,   192,   365,   372,   269,    53,
     377,   157,    47,    48,    49,    50,    51,    26,   378,   331,
     104,    62,    47,   193,    49,    50,   194,   228,   229,    52,
     215,    99,   100,   108,    47,    48,    49,    50,    51,    52,
      53,   236,   237,   116,   390,   126,   119,   404,   303,   304,
      53,    52,   126,    76,   123,   125,   267,   142,   101,   413,
     391,   143,    53,   127,   128,   129,   130,   131,   268,   145,
     127,   128,   129,   130,   131,   392,   153,   154,   126,   132,
       8,    99,   100,   155,   156,   160,   169,   264,   133,     9,
     174,  -209,   148,    10,    11,   133,   127,   128,   129,   130,
     131,    12,    -4,    76,   390,     8,   172,    66,   140,   175,
     234,   149,   150,   151,     9,   267,   267,   179,    10,    11,
     391,   133,   177,   178,   180,   181,    12,   268,   268,   267,
     182,    76,   382,   185,   199,    76,    67,    68,    69,    70,
     200,   268,   188,   201,   202,   203,   396,   100,   204,    71,
     210,    72,    73,    74,    67,    68,    69,    70,   212,   218,
     220,   222,   224,   226,   227,   235,   245,   249,   240,    72,
      73,   242,   260,   247,   248,   257,   252,   263,   283,   295,
     318,   314,   299,   300,   301,   310,   315,   319,   321,   329,
     322,   324,   325,   333,   326,   327,   336,   330,   338,   350,
     351,   348,   354,   279,   356,   285,   358,   359,   291,   362,
     363,   364,   368,   373,   381,   379,   380,   361,   405,   387,
     388,   399,   408,     5,   403,   266,   416,   366,   337,   417,
     367,   221,   259,   335,    34,   334,   376,   317,   409,   225,
     251,     0,   183,   256,   355,   124,   357,   360
  };

  const short
  parser::yycheck_[] =
  {
      24,    25,   178,   307,    89,   110,   307,    84,   238,     5,
      54,   307,    36,     3,     5,   185,   307,    34,    62,   307,
       3,     9,    10,    11,    35,     3,     3,   373,    52,     3,
       3,    13,    14,    16,    45,    15,    60,     4,   384,    27,
       3,    85,    16,     7,     8,    33,     3,    27,    92,    27,
      38,    42,     4,    35,    50,    45,    44,   142,   143,   229,
     137,   166,    45,    20,    21,    22,    23,    24,    46,    46,
      37,    45,    45,     0,    37,    99,   100,    65,    66,   103,
      37,   105,     5,    47,   260,   389,    38,     0,   389,    77,
     134,    48,     3,   389,    82,   139,   400,   401,   389,   400,
     401,   389,     3,   208,   400,   401,    18,    27,    19,   400,
     401,    12,   400,   401,    37,    15,   160,     0,    38,    37,
      36,   145,    33,    24,    42,    35,   170,    27,     3,    39,
     174,     3,    33,    45,    34,     3,   241,    12,   243,   244,
     164,   246,   186,   373,   188,    65,    66,   171,   172,    24,
     138,    19,   382,   383,     3,   199,   200,    36,    33,    13,
      14,   393,    36,    12,    16,    33,   396,    16,    17,    13,
      14,   276,     3,     4,     5,    24,   281,   409,     3,   203,
      35,    35,   287,    38,    33,    39,   210,    12,   293,    20,
      21,    22,    23,    24,    25,    39,    27,    10,    11,    24,
       3,     4,     3,     4,     5,    45,    37,    36,    33,     3,
      41,   235,    32,   237,     3,     4,     5,    48,    12,    20,
      21,    22,    23,    24,    27,   249,    27,   271,     3,     3,
      24,    20,    21,    22,    23,    24,    37,    12,    27,    33,
      41,    16,    17,     9,     3,     4,     5,    48,    37,    24,
      36,    35,    41,    41,    40,    13,    14,    45,    33,    48,
      37,    20,    21,    22,    23,    24,    13,    14,    27,    13,
      14,   315,   377,   378,     3,   299,    37,   301,    37,     3,
      38,    39,    41,    37,     3,    37,   310,    13,    14,    48,
      37,    20,    21,    22,    23,    24,    20,    21,    22,    23,
      24,    20,    21,    22,    23,    24,    13,    14,    37,    38,
     381,    15,    38,    37,    38,     3,   387,   388,    37,    48,
      13,    14,    36,    27,    48,     3,    40,   351,    32,    48,
     354,    38,    20,    21,    22,    23,    24,     3,   362,     5,
      37,   365,    20,    21,    22,    23,    24,    38,    39,    37,
      38,    13,    14,     5,    20,    21,    22,    23,    24,    37,
      48,    38,    39,     4,     3,     3,     3,   391,    38,    39,
      48,    37,     3,    35,     3,     3,    15,    32,    40,   403,
      19,    32,    48,    21,    22,    23,    24,    25,    27,    37,
      21,    22,    23,    24,    25,    34,     5,     5,     3,    37,
       3,    13,    14,     5,     5,    27,     5,    38,    46,    12,
      42,    36,     3,    16,    17,    46,    21,    22,    23,    24,
      25,    24,     0,    35,     3,     3,    39,    14,    40,    39,
      33,    22,    23,    24,    12,    15,    15,     4,    16,    17,
      19,    46,    42,    36,    41,    18,    24,    27,    27,    15,
      18,    35,    32,    39,    36,    35,    28,    29,    30,    31,
      37,    27,    27,    39,    39,    39,    32,    14,    39,    41,
      39,    43,    44,    45,    28,    29,    30,    31,    39,    38,
       5,     4,    39,     3,    23,    40,    49,    39,    41,    43,
      44,    41,    36,    42,    42,    38,    42,    42,    39,    39,
       5,    38,    40,    39,    39,    36,    39,    39,    38,     3,
      39,    38,    38,     3,    36,    39,     4,    38,    33,     3,
      26,    40,    39,    37,    42,     5,    42,     3,     5,    40,
      38,    33,    36,    36,    32,    36,    36,    50,    33,    32,
      32,    38,    33,     1,    40,   237,    33,   342,   305,    38,
     342,   177,   221,   301,    11,   300,   353,   278,   396,   180,
     210,    -1,   132,   212,   319,    77,   322,   327
  };

  const signed char
  parser::yystos_[] =
  {
       0,    34,    52,    53,    54,    53,     0,     0,     3,    12,
      16,    17,    24,    56,    64,    65,    68,    74,    75,    82,
      85,    89,    91,     0,    36,    40,     3,    37,    71,   124,
      76,    77,   124,    45,    78,   124,    36,    10,    11,    69,
      70,    36,     7,     8,    47,    92,    93,    20,    21,    22,
      23,    24,    37,    48,   110,   124,     4,     5,    25,    27,
      37,    41,   110,   123,    71,    13,    14,    28,    29,    30,
      31,    41,    43,    44,    45,    73,    35,    39,    55,   101,
      18,    16,    45,    78,    16,   110,    71,    36,    36,    32,
       3,    57,   124,     9,    37,    37,    37,    37,   110,    13,
      14,    40,    55,    41,    37,    35,   110,   122,     5,    83,
      84,    39,    55,    38,    71,    71,     4,   125,   126,     3,
       5,    37,    72,     3,    77,     3,     3,    21,    22,    23,
      24,    25,    37,    46,    79,    80,    81,    16,    45,    79,
      40,    55,    32,    32,    54,    37,    58,    55,     3,    22,
      23,    24,    90,     5,     5,     5,     5,    38,   110,   110,
      27,     4,     5,    27,    37,    41,   106,   107,   110,     5,
     110,    39,    39,   114,    42,    39,   114,    42,    36,     4,
      41,    18,    18,    80,    55,    39,    79,    55,    27,    54,
      54,    33,     3,    21,    24,    38,    59,    60,   110,    36,
      37,    39,    39,    39,    39,    55,    38,   108,   109,   110,
      39,   114,    39,    86,    55,    38,   110,   110,    38,    55,
       5,    73,     4,   126,    39,   108,     3,    23,    38,    39,
      81,    55,    55,    33,    33,    40,    38,    39,    55,    55,
      41,   111,    41,   115,   110,    49,   118,    42,    42,    39,
     114,   107,    42,     3,    87,    88,   109,    38,     4,    72,
      36,     4,    38,    42,    38,   110,    60,    15,    27,    32,
      61,   127,     3,    27,    46,    94,    95,    96,    99,    37,
      42,   112,   113,    39,   114,     5,    42,   116,   117,   114,
     114,     5,    50,   119,   120,    39,   114,   121,   110,    40,
      39,    39,   126,    38,    39,    34,    62,    63,   127,    55,
      36,    97,     3,    46,    38,    39,   114,    97,     5,    39,
     114,    38,    39,   114,    38,    38,    36,    39,   114,     3,
      38,     5,   110,     3,    88,    87,     4,    62,    33,     3,
      56,    66,    67,    68,    74,    82,    89,   110,    40,    98,
       3,    26,   100,    55,    39,   113,    42,   117,    42,     3,
     120,    50,    40,    38,    33,    40,    69,    70,    36,     3,
       4,    27,   110,    36,   102,   103,    96,   110,   110,    36,
      36,    32,    32,   101,   127,   114,   114,    32,    32,    63,
       3,    19,    34,   104,   105,   127,    32,   127,   101,    38,
      63,    63,    33,    40,   110,    33,    33,   105,    33,   104,
     127,    33,    33,   110,    37,    33,    33,    38
  };

  const signed char
  parser::yyr1_[] =
  {
       0,    51,    52,    52,    53,    54,    54,    54,    54,    54,
      54,    54,    54,    55,    55,    56,    57,    58,    58,    58,
      59,    59,    60,    60,    60,    60,    61,    61,    61,    62,
      62,    63,    63,    63,    63,    63,    63,    64,    64,    65,
      65,    66,    66,    67,    67,    68,    69,    70,    71,    71,
      71,    71,    71,    71,    71,    72,    72,    72,    73,    73,
      73,    73,    73,    73,    74,    74,    74,    74,    74,    74,
      74,    74,    74,    75,    75,    75,    75,    76,    76,    77,
      77,    78,    78,    79,    79,    79,    80,    80,    81,    81,
      81,    81,    81,    81,    81,    81,    81,    82,    82,    83,
      83,    84,    84,    85,    86,    86,    86,    86,    87,    87,
      88,    88,    89,    90,    90,    90,    90,    91,    91,    92,
      93,    93,    94,    94,    95,    95,    96,    96,    96,    96,
      97,    97,    98,    98,    98,    98,    99,    99,   100,   100,
     101,   101,   102,   102,   102,   103,   103,   103,   103,   103,
     103,   103,   104,   104,   105,   105,   105,   106,   106,   107,
     107,   107,   107,   107,   108,   108,   109,   109,   110,   110,
     110,   110,   110,   110,   110,   110,   110,   110,   110,   110,
     111,   111,   112,   112,   113,   114,   114,   115,   115,   116,
     116,   117,   118,   118,   119,   119,   120,   121,   121,   122,
     122,   123,   123,   123,   124,   124,   125,   125,   125,   126,
     126,   127,   127
  };

  const signed char
  parser::yyr2_[] =
  {
       0,     2,     2,     3,     1,     2,     2,     2,     2,     2,
       2,     2,     0,     1,     0,     7,     1,     3,     2,     0,
       3,     1,     1,     3,     1,     1,     2,     3,     4,     1,
       1,     2,     2,     2,     2,     2,     0,     6,     1,     5,
       6,     6,     1,     5,     6,     2,     2,     1,     3,     3,
       6,     6,     3,     3,     3,     4,     5,     7,     1,     1,
       1,     1,     1,     1,     3,     3,     3,     3,     6,     4,
       6,     4,     6,     3,     5,     5,     6,     3,     1,     1,
       3,     1,     2,     1,     3,     4,     3,     1,     1,     1,
       1,     1,     1,     1,     1,     3,     3,     4,     6,     2,
       0,     3,     1,     7,     0,     2,     2,     4,     3,     1,
       3,     3,    10,     1,     1,     1,     1,     2,     0,     3,
       1,     0,     2,     0,     4,     1,     3,     1,     2,     1,
       2,     0,     2,     2,     2,     0,     2,     3,     2,     0,
       2,     5,     5,     4,     1,     2,     3,     3,     5,     4,
       4,     0,     2,     1,     3,     2,     4,     3,     1,     1,
       1,     1,     1,     3,     2,     0,     3,     1,     1,     5,
       5,     7,     7,     7,     7,     3,     3,     3,     1,     1,
       4,     2,     3,     1,     6,     1,     0,     4,     2,     3,
       1,     1,     4,     2,     3,     1,     3,     5,     1,     3,
       3,     4,     4,     2,     1,     3,     1,     3,     5,     1,
       0,     1,     1
  };


#if PYTYPEDEBUG || 1
  // YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
  // First, the terminals, then, starting at \a YYNTOKENS, nonterminals.
  const char*
  const parser::yytname_[] =
  {
  "\"end of file\"", "error", "\"invalid token\"", "NAME", "NUMBER",
  "STRING", "LEXERROR", "ASYNC", "CLASS", "DEF", "ELSE", "ELIF", "IF",
  "OR", "AND", "PASS", "IMPORT", "FROM", "AS", "RAISE", "NOTHING",
  "NAMEDTUPLE", "COLL_NAMEDTUPLE", "NEWTYPE", "TYPEDDICT", "TYPEVAR",
  "ARROW", "ELLIPSIS", "EQ", "NE", "LE", "GE", "INDENT", "DEDENT",
  "TRIPLEQUOTED", "TYPECOMMENT", "':'", "'('", "')'", "','", "'='", "'['",
  "']'", "'<'", "'>'", "'.'", "'*'", "'@'", "'?'", "'{'", "'}'", "$accept",
  "start", "unit", "alldefs", "maybe_type_ignore", "classdef",
  "class_name", "parents", "parent_list", "parent", "maybe_class_funcs",
  "class_funcs", "funcdefs", "if_stmt", "if_and_elifs", "class_if_stmt",
  "class_if_and_elifs", "if_cond", "elif_cond", "else_cond", "condition",
  "version_tuple", "condition_op", "constantdef", "importdef",
  "import_items", "import_item", "import_name", "from_list", "from_items",
  "from_item", "alias_or_constant", "maybe_string_list", "string_list",
  "typevardef", "typevar_args", "typevar_kwargs", "typevar_kwarg",
  "funcdef", "funcname", "decorators", "decorator", "maybe_async",
  "params", "param_list", "param", "param_type", "param_default",
  "param_star_name", "return", "typeignore", "maybe_body", "empty_body",
  "body", "body_stmt", "type_parameters", "type_parameter",
  "maybe_type_list", "type_list", "type", "named_tuple_fields",
  "named_tuple_field_list", "named_tuple_field", "maybe_comma",
  "coll_named_tuple_fields", "coll_named_tuple_field_list",
  "coll_named_tuple_field", "typed_dict_fields", "typed_dict_field_dict",
  "typed_dict_field", "maybe_typed_dict_kwarg", "type_tuple_elements",
  "type_tuple_literal", "dotted_name", "getitem_key", "maybe_number",
  "pass_or_ellipsis", YY_NULLPTR
  };
#endif


#if PYTYPEDEBUG
  const short
  parser::yyrline_[] =
  {
       0,   135,   135,   136,   140,   144,   145,   146,   147,   153,
     154,   155,   160,   164,   165,   172,   182,   193,   194,   195,
     199,   200,   204,   205,   206,   207,   214,   215,   216,   220,
     221,   225,   226,   231,   232,   237,   238,   243,   246,   251,
     255,   268,   271,   276,   280,   292,   296,   300,   304,   307,
     310,   313,   316,   317,   318,   322,   323,   324,   330,   331,
     332,   333,   334,   335,   339,   343,   347,   351,   355,   359,
     363,   367,   371,   378,   382,   386,   392,   401,   402,   406,
     407,   412,   413,   420,   421,   422,   426,   427,   431,   432,
     435,   438,   441,   444,   447,   450,   451,   455,   456,   460,
     461,   465,   466,   470,   477,   478,   479,   480,   484,   485,
     489,   491,   495,   509,   510,   511,   512,   516,   517,   521,
     525,   526,   530,   531,   543,   544,   548,   549,   550,   551,
     555,   556,   560,   561,   562,   563,   567,   568,   572,   573,
     577,   578,   585,   586,   587,   591,   592,   593,   594,   595,
     596,   597,   601,   602,   606,   607,   608,   612,   613,   617,
     618,   620,   621,   623,   630,   631,   635,   636,   640,   644,
     648,   652,   656,   660,   664,   668,   669,   670,   671,   672,
     676,   677,   681,   682,   686,   690,   691,   695,   696,   700,
     703,   707,   711,   712,   716,   721,   725,   729,   730,   737,
     738,   747,   752,   758,   765,   766,   780,   781,   786,   794,
     795,   799,   800
  };

  void
  parser::yy_stack_print_ () const
  {
    *yycdebug_ << "Stack now";
    for (stack_type::const_iterator
           i = yystack_.begin (),
           i_end = yystack_.end ();
         i != i_end; ++i)
      *yycdebug_ << ' ' << int (i->state);
    *yycdebug_ << '\n';
  }

  void
  parser::yy_reduce_print_ (int yyrule) const
  {
    int yylno = yyrline_[yyrule];
    int yynrhs = yyr2_[yyrule];
    // Print the symbols being reduced, and their result.
    *yycdebug_ << "Reducing stack by rule " << yyrule - 1
               << " (line " << yylno << "):\n";
    // The symbols being reduced.
    for (int yyi = 0; yyi < yynrhs; yyi++)
      YY_SYMBOL_PRINT ("   $" << yyi + 1 << " =",
                       yystack_[(yynrhs) - (yyi + 1)]);
  }
#endif // PYTYPEDEBUG

  parser::symbol_kind_type
  parser::yytranslate_ (int t)
  {
    // YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to
    // TOKEN-NUM as returned by yylex.
    static
    const signed char
    translate_table[] =
    {
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      37,    38,    46,     2,    39,     2,    45,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,    36,     2,
      43,    40,    44,    48,    47,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,    41,     2,    42,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,    49,     2,    50,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35
    };
    // Last valid token kind.
    const int code_max = 290;

    if (t <= 0)
      return symbol_kind::S_YYEOF;
    else if (t <= code_max)
      return YY_CAST (symbol_kind_type, translate_table[t]);
    else
      return symbol_kind::S_YYUNDEF;
  }

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
} // pytype
#line 3302 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

#line 803 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"


void pytype::parser::error(const location& loc, const std::string& msg) {
  ctx->SetErrorLocation(loc);
  pytype::Lexer* lexer = pytypeget_extra(scanner);
  if (lexer->error_message_) {
    PyErr_SetObject(ctx->Value(pytype::kParseError), lexer->error_message_);
  } else {
    PyErr_SetString(ctx->Value(pytype::kParseError), msg.c_str());
  }
}

namespace {

PyObject* StartList(PyObject* item) {
  return Py_BuildValue("[N]", item);
}

PyObject* AppendList(PyObject* list, PyObject* item) {
  PyList_Append(list, item);
  Py_DECREF(item);
  return list;
}

PyObject* ExtendList(PyObject* dst, PyObject* src) {
  // Add items from src to dst (both of which must be lists) and return src.
  // Borrows the reference to src.
  Py_ssize_t count = PyList_Size(src);
  for (Py_ssize_t i=0; i < count; ++i) {
    PyList_Append(dst, PyList_GetItem(src, i));
  }
  Py_DECREF(src);
  return dst;
}

}  // end namespace
